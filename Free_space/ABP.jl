using Random 
using LinearAlgebra
using CSV, DataFrames
using ArgParse
import Statistics
using Dates
using Printf

const sqrt3 = sqrt(3.0)
@inline function unitrand(::Type{Float64})
    return sqrt3 * (2.0 * rand(Float64) - 1.0)
end
@inline function randbetween(a, b)
    a,b=promote(a,b)
    return rand(typeof(a))*(b-a)+a 
end

function bd!(x, y, theta, x0, y0, theta0, ampDt, ampDr,v, dt)
    N = length(x)
    msdx = 0.0
    msdy = 0.0
    meanx = 0.0
    meany = 0.0

    for j in 1:N
        
        x[j] += ampDt * unitrand(Float64) + v*cos(theta[j])*dt
        y[j] += ampDt * unitrand(Float64) + v*sin(theta[j])*dt
        theta[j] += ampDr * unitrand(Float64)

        msdx += (x[j] - x0[j])^2
        msdy += (y[j] - y0[j])^2
        meanx += x[j] - x0[j]
        meany += y[j] - y0[j]

    end

    return msdx / N, msdy / N, meanx / N, meany / N
end
function simulate(Dt, Dr, N, tf, dt, v)
    L = 1.0
    Nstep = Int64(floor(tf/dt))
    ampDt = Float64(sqrt(2*Dt*dt))
    ampDr = Float64(sqrt(2*Dr*dt))
    x0 = [randbetween(0, L) for _ in 1:N]
    y0 = [randbetween(0, L) for _ in 1:N]
    theta0 = [unitrand(Float64) for _ in 1:N]
    x = copy(x0)
    y = copy(y0)
    theta = copy(theta0)
    t = 0.0
    t_arr = zeros(Nstep)
    msdx = zeros(Nstep)
    msdy = zeros(Nstep)
    msd = zeros(Nstep)
    meanx = zeros(Nstep)
    meany = zeros(Nstep)
    for i in 1:Nstep
        t_arr[i] = t
        msdx[i], msdy[i],  meanx[i], meany[i] = bd!(x, y, theta, x0, y0, theta0, ampDt, ampDr,v, dt)
        msd[i] = msdx[i] + msdy[i]
        if i % 1000 == 0
            @info "Timestep $i, time = $(round(t, digits=3)) : MSD_x = $(round(msdx[i], digits=4)), MSD_y = $(round(msdy[i], digits=4)), MSD = $(round(msd[i], digits=4))"
        end
        t += dt
    end
    return t_arr , msdx, msdy, msd, meanx, meany
end
function parse_command_line()
    s = ArgParseSettings()

    @add_arg_table! s begin
        "--Dt"
            help = "Diffusion constant"
            arg_type = Float64
            default = 1.00
        "--Dr"
            help ="Rotational Diffusion constant"
            arg_type = Float64
            default = 1.00
        "--dt"
            help = "time step"
            arg_type = Float64
            default = 0.001
        "--tf"
            help = "total time"
            arg_type = Float64
            default = 100.0
        "--N"
            help = "No of particles"
            arg_type = Int
            default = 10000
        "--v"
            help = "propulsion velocity"
            arg_type = Float64
            default = 1.0
    end
    return parse_args(ARGS,s)
end
function main()
    args = parse_command_line()
    Dt = args["Dt"]
    dt = args["dt"]
    tf = args["tf"]
    N = args["N"]
    Dr = args["Dr"]
    v = args["v"]
    start_time = now()
    t_arr, msdx, msdy, msd, meanx, meany = simulate(Dt, Dr, N, tf, dt, v)
    end_time = now()

    df = DataFrame(
    time = t_arr,
    mean_dx = meanx,
    mean_dy = meany,
    msd_x = msdx,
    msd_y = msdy,
    msd = msd
)
CSV.write("msd_data_D_$(Dt)_Dr_$(Dr)_v_$(v)_N_$(N)_dt_$( @sprintf("%.4f", dt) ).csv", df)
    elapsed = end_time - start_time
    println("Elapsed time: $elapsed")
end


main()
