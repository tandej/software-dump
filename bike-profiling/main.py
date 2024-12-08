import math
import matplotlib.pyplot as plt

vMeterPSecond: float = 0
totalEnergyJoules: float = 0

######

prevLinAccel: float = 0  # for trapezoidal estimation in numerical integration
prevPowerWatts: float = 0

def numInt(
    linAccelRadianPSecondSquared: float, powerWatts: float, timestepSeconds: float
):
    # writes to global state ahhh
    global vMeterPSecond, totalEnergyJoules, prevLinAccel, prevPowerWatts

    vMeterPSecond += (prevLinAccel * timestepSeconds) + (
        0.5 * timestepSeconds * (linAccelRadianPSecondSquared - prevLinAccel)
    )

    totalEnergyJoules += (prevPowerWatts * timestepSeconds) + (
        0.5 * timestepSeconds * (powerWatts - prevPowerWatts)
    )

    prevLinAccel = linAccelRadianPSecondSquared
    prevPowerWatts = powerWatts

#####

# system constants
kTnewtonMetersPAmp: float = 1.2/12.8
kVradiansPSecondPVolt: float = (2750 / 36) * (2 * math.pi) / 60 # rpm -> radps
gearing: float = 120/11  # reduction is >1
wheelRadiusMeters: float = .2
bikeMassKg: float = 20
stallCurrentAmps: float = 12.8
mechanicalEfficiency: float = .85 # proportion of torque not lost to heat etc
batteryResistanceOhms: float = .02
batteryRestingVoltage: float = 36

#####

prevCurrentDraw: float = 0

# P = τ * ω
# τ = k_t * I
# a_ang = τ/m_ang
# ω_free = k_v * V
# I = (1 - (ω/ω_free)) * I_stall

def systemLoop(timestep: float):
    global prevCurrentDraw

    freeSpeed = (kVradiansPSecondPVolt) * (batteryRestingVoltage - (batteryResistanceOhms * prevCurrentDraw)) / gearing
    current = (1 - ((vMeterPSecond * wheelRadiusMeters) / freeSpeed)) * stallCurrentAmps
    torque = kTnewtonMetersPAmp * current * mechanicalEfficiency * gearing

    print("current" + str(current))
    print("torque" + str(torque))

    prevCurrentDraw = current
    
    numInt((torque / wheelRadiusMeters) / (bikeMassKg) / gearing, torque * (vMeterPSecond * wheelRadiusMeters), timestep)

fig, ax = plt.subplots()

timeData = []
currentData = []
energyData = []
velData = []

for i in range(10000):
    systemLoop(.01)
    timeData.append(i * .01)
    currentData.append(prevCurrentDraw)
    energyData.append(totalEnergyJoules)
    velData.append(vMeterPSecond)

ax.scatter(timeData, currentData, c="blue", label="current")
#ax.scatter(timeData, energyData, c="red", label="energy")
ax.scatter(timeData, velData, c="green", label="velocity")

ax.legend()

plt.show()
