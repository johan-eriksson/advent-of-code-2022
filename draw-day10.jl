# %%
using Test

# %%
f = readlines("day10.input");

# %%
mutable struct Cpu
    score::Int64
    cycle::Int64
    x::Int64 
    Cpu() = new(0, 1, 1)
end


# %%
function increment_cycle(cpu::Cpu)

    print(abs((cpu.x + 1) - cpu.cycle%40) < 2 ? "X" : " ")
    if cpu.cycle % 40 == 0
        print('\n')
    end

    cpu.cycle += 1
    if (20+cpu.cycle)%40 == 0 && cpu.cycle < 271
        cpu.score += cpu.cycle*cpu.x
    end
end

# %%
function noop(cpu::Cpu)
    increment_cycle(cpu)
end

# %%
function addx(cpu::Cpu, val)
    increment_cycle(cpu)
    increment_cycle(cpu)
    cpu.x += val
end

# %%
function run(cpu::Cpu, instructions)
    for instruction in instructions
        if instruction == "noop"
            noop(cpu)
        else
            addx(cpu, parse(Int64, last(split(instruction))))
        end
    end
end

# %%
function draw_image(input)
    cpu = Cpu()
    run(cpu, input)
end 

draw_image(f)

