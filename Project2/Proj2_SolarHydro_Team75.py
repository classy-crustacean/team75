import math

# monkey code dictionaries
pumpGrades    = ('cheap', 'value', 'standard', 'high-grade', 'premium')
turbineGrades = ('meh', 'good', 'fine', 'superb', 'mondo')
pipeGrades    = ('salvage', 'questionable', 'better', 'nice', 'outstanding', 'glorious')
pipeDiameters = (0.10, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00)

pumps = {
    'cheap'     : {'efficiency': 0.80, 20: 200, 30: 220, 40: 242, 50: 266, 60: 293, 70: 322, 80: 354, 90: 390, 100: 429, 110: 472, 120: 519},
    'value'     : {'efficiency': 0.83, 20: 240, 30: 264, 40: 290, 50: 319, 60: 351, 70: 387, 80: 425, 90: 468, 100: 514, 110: 566, 120: 622},
    'standard'  : {'efficiency': 0.86, 20: 288, 30: 317, 40: 348, 50: 383, 60: 422, 70: 464, 80: 510, 90: 561, 100: 617, 110: 679, 120: 747},
    'high-grade': {'efficiency': 0.89, 20: 346, 30: 380, 40: 418, 50: 460, 60: 506, 70: 557, 80: 612, 90: 673, 100: 741, 110: 815, 120: 896},
    'premium'   : {'efficiency': 0.92, 20: 415, 30: 456, 40: 502, 50: 552, 60: 607, 70: 668, 80: 735, 90: 808, 100: 889, 110: 978, 120: 1076}
    }
turbines = {
    'meh'    :{'efficiency': .83, 20:360, 30:396, 40:436, 50:479, 60:527,  70:580,  80:638,  90:702,  100:772,  110:849,  120:934},
    'good'   :{'efficiency': .86, 20:432, 30:475, 40:523, 50:575, 60:632,  70:696,  80:765,  90:842,  100:926,  110:1019, 120:1120},
    'fine'   :{'efficiency': .89, 20:518, 30:570, 40:627, 50:690, 60:759,  70:835,  80:918,  90:1010, 100:1111, 110:1222, 120:1345},
    'superb': {'efficiency': .94, 20:622, 30:684, 40:753, 50:828, 60:911,  70:1002, 80:1102, 90:1212, 100:1333, 110:1467, 120:1614},
    'mondo'  :{'efficiency': .94, 20:746, 30:821, 40:903, 50:994, 60:1093, 70:1202, 80:1322, 90:1455, 100:1600, 110:1760, 120:1936}
    }
bends = {
    20: {'pipeLoss': .10, 0.10:1.00, 0.25:1.49, 0.50:4.93, 0.75:14, 1.00:32, 1.25:62, 1.50:107, 1.75:169, 2.00:252, 2.25:359, 2.50:492, 2.75:654, 3.00:849},
    30: {'pipeLoss': .15, 0.10:1.05, 0.25:1.57, 0.50:5.17, 0.75:15, 1.00:34, 1.25:65, 1.50:112, 1.75:178, 2.00:265, 2.25:377, 2.50:516, 2.75:687, 3.00:892},
    45: {'pipeLoss': .20, 0.10:1.10, 0.25:1.64, 0.50:5.43, 0.75:16, 1.00:36, 1.25:69, 1.50:118, 1.75:187, 2.00:278, 2.25:396, 2.50:542, 2.75:721, 3.00:936},
    60: {'pipeLoss': .22, 0.10:1.16, 0.25:1.73, 0.50:5.70, 0.75:16, 1.00:38, 1.25:72, 1.50:124, 1.75:196, 2.00:292, 2.25:415, 2.50:569, 2.75:757, 3.00:983},
    75: {'pipeLoss': .27, 0.10:1.22, 0.25:1.81, 0.50:5.99, 0.75:17, 1.00:39, 1.25:76, 1.50:130, 1.75:206, 2.00:307, 2.25:436, 2.50:598, 2.75:795, 3.00:1032},
    90: {'pipeLoss': .30, 0.10:1.28, 0.25:1.90, 0.50:7.00, 0.75:18, 1.00:41, 1.25:80, 1.50:137, 1.75:216, 2.00:322, 2.25:458, 2.50:628, 2.75:835, 3.00:1084}
    }
pipes = {
    'salvage'      :{'frictionFactor':.05 , 0.10:1.00, 0.25:1.20, 0.50:2.57, 0.75:6.30, 1.00:14, 1.25:26, 1.50:43 , 1.75:68 , 2.00:102, 2.25:144, 2.50:197, 2.75:262, 3.00:340},
    'questionable' :{'frictionFactor':.03 , 0.10:1.20, 0.25:1.44, 0.50:3.08, 0.75:7.56, 1.00:16, 1.25:31, 1.50:52 , 1.75:82 , 2.00:122, 2.25:173, 2.50:237, 2.75:315, 3.00:408},
    'better'       :{'frictionFactor':.02 , 0.10:1.44, 0.25:1.72, 0.50:3.70, 0.75:9.07, 1.00:20, 1.25:37, 1.50:63 , 1.75:98 , 2.00:146, 2.25:208, 2.50:284, 2.75:378, 3.00:490},
    'nice'         :{'frictionFactor':.01 , 0.10:2.16, 0.25:2.58, 0.50:5.55, 0.75:14.0, 1.00:29, 1.25:55, 1.50:94 , 1.75:148, 2.00:219, 2.25:311, 2.50:426, 2.75:567, 3.00:735},
    'outstanding'  :{'frictionFactor':.005, 0.10:2.70, 0.25:3.32, 0.50:6.94, 0.75:17.0, 1.00:37, 1.25:69, 1.50:117, 1.75:185, 2.00:274, 2.25:389, 2.50:533, 2.75:708, 3.00:919},
    'glorious'     :{'frictionFactor':.002, 0.10:2.97, 0.25:3.55, 0.50:7.64, 0.75:19.0, 1.00:40, 1.25:76, 1.50:129, 1.75:203, 2.00:302, 2.25:428, 2.50:586, 2.75:779, 3.00:1011}
    }

# site dictionary for pipe installations
siteDictionary = {
    1:{'length':67.8, 'performanceRating':80,  'angle1':30, 'angle2':30}, 
    3:{'length':129,  'performanceRating':120, 'angle1':45, 'angle2':45}}

# Joe's magic user inputs
def getUserInput():
    print("""Choices for site:
    Zone 1
    Zone 3""")
    sitesInput = input("Enter number for zone to consider. If nothing is entered, site 1 will be assumed: ")
    site = 0

    # 
    if sitesInput.__contains__('1'):
        site = 1
    if sitesInput.__contains__('3'):
        site = 3
    if sitesInput.__contains__('2'):
        print("Site 2 is on a native american burial ground: You will run out of money in legal fees before you finish; you are now on site 1.")
        site = 1
    
    try:
        budget = int(input("What is your budget? (If no budget, just press enter): "))
    except ValueError:
        budget = 1000000000 # really big value that will be bigger than any price

    
    return {'site': site, 'budget': budget}
userInput = getUserInput()

# changing input to site 1 if there isn't a site entered
if userInput['site'] == 1:
    pass
elif userInput['site'] == 3:
    pass
else:
    userInput['site'] = 1

# inputs, now they are actually user inputs
depth        = int(input('Input depth: ')) # depth of the reservoir in meters
fillTime     = float(input('Enter fill time, in hours: '))   # time, in hours for both filling and draining
turbineFlow  = float(input('Enter turbine flow: '))   # turbine volumetric flow
pumpFlow     = float(input('Enter pump flow: '))   # pump volumetric flow

# assumed constants
g            = 9.81 # gravity, for the love of god dont make this an input
waterDensity = 1000 # density of water, kg per m^3
energyOut    = 120 # mwh required

# big monstrous equations
def energyIn(energyOut, pipeFriction, pipeLength, pipeDiameter, bendConstant1, bendConstant2,  mass, pumpEfficiency, turbineEfficiency, velocityOut, velocityIn):
    energy = (
        (energyOut / turbineEfficiency) + (mass / 2) * (velocityOut * velocityOut + velocityIn * velocityIn) * (pipeFriction * (pipeLength / pipeDiameter) + bendConstant1 + bendConstant2 )
        ) / pumpEfficiency
    return energy

# efficiency
def efficiency(energyOut, energyIn):
    return (energyOut / energyIn) * 100

# mass equation
def mass (turbineFlow, waterDensity, t):
    return turbineFlow * waterDensity * t

# velocity out
def velocityOut (turbineFlow, diameter):
    return (4 * turbineFlow) / (diameter * diameter * math.pi)

# velocity in
def velocityIn (pumpFlow, diameter):
    return (4 * pumpFlow) / (diameter * diameter * math.pi)

# area of reservoir
def reservoirArea (mass, waterDensity):
    return (mass / waterDensity) / depth

# converts joules to mwh
def mwh(joules):
    return joules / (1E6 * 60 * 60)

# converts mwh to joules
def joules(mwh):
    return mwh * 3.6E9

# converts hours to seconds
def seconds(hours):
    return hours * 60 * 60

# cost calculations
def pumpCost(pumpGrade, performanceRatingUp, flowRateUp):
    cost = flowRateUp * (pumps[pumpGrade][performanceRatingUp])
    return cost

def turbineCost(turbineGrade, performanceRatingDown, flowRateDown):
    cost = flowRateDown * (turbines[turbineGrade][performanceRatingDown])
    return cost

def fittingCost(angle, diameter):
    cost = bends[angle][diameter]
    return cost

def pipeCost(grade, diameter, length):
    cost = length * (pipes[grade][diameter])
    return cost

def costEfficiency(cost, efficiency):
    return cost / efficiency

def wallCost(reservoirArea, height):
    costPerMeter = 0 
    depth = height
    circumference = 2 * math.sqrt(reservoirArea * math.pi)
    if height <= 5:
        costPerMeter = (depth) * (30)/(5)
    elif height <= 7.5:
        costPerMeter = 30 + (depth - 5) * (30)/(2.5)
    elif height <= 10:
        costPerMeter = 30 + 60 + (depth - 7.5)* (35)/(2.5)
    elif height <= 12.5:
        costPerMeter = 30 + 60 + 95 + (depth - 10) * (40)/(2.5)
    elif height <= 15:
        costPerMeter = 30 + 60 + 95 + 135 + (depth - 12.5) * (45)/(2.5)
    elif height <= 17.5:
        costPerMeter = 30 + 60 + 95 + 135 + 180 + (depth - 15) * (70)/(2.5)
    else:
        costPerMeter = 30 + 60 + 95 + 135 + 180 + 250 + (depth - 17.5) * (90)/(2.5)
    return costPerMeter * circumference

# site 1 calculations for site specific costs
def site1cost(reservoirArea):
    # costs for land development
    cost = 0
    cost += 40000 # access road
    cost += 100000 # pumphouse
    cost += (reservoirArea * .25) # reservoir area
    cost += 10000 # random testing 
    cost += 67.08 * 500 # pipe installation on ground
    return cost

# site 3 calculations for site specific costs
def site3cost(reservoirArea):
    # cost of land development
    cost = 0
    cost += 150000 # access road
    cost += 100000 # pumphouse
    cost += (reservoirArea * .3) # reservoir area development
    cost += (reservoirArea * 1.6 * .2) # tree replanting
    cost += 118.2 * 500 # pipe installation on ground
    cost += 1381 * 250 # pipe installation off of ground
    return cost

# big cost equation
def masterCost(pumpGrade, performanceRatingUp, flowRateUp, turbineGrade, performanceRatingDown, flowRateDown, angle1, angle2,  pipeGrade, diameter, length, depth, site, area):
    totalCost = 0

    # adds costs that depend on grades
    totalCost += pumpCost(pumpGrade, performanceRatingUp, flowRateUp)
    totalCost += turbineCost(turbineGrade, performanceRatingDown, flowRateDown)
    totalCost += fittingCost(angle1, diameter)
    totalCost += fittingCost(angle2, diameter)
    totalCost += pipeCost(pipeGrade, diameter, (length + depth))
    totalCost += wallCost(area, depth)
    
    # adds site specific costs
    if site == 1:
        totalCost += site1cost(reservoirArea(mass(turbineFlow, waterDensity, fillTime), waterDensity))
    else:
        totalCost += site3cost(reservoirArea(mass(turbineFlow, waterDensity, fillTime), waterDensity))
    return totalCost
 
# declares the starting efficiency as zero for comparisons
efficiencyCheck = 0
currentGrades = 0

# runs cost and efficiency calculations for every pipe diameter and grade of pipe, pump, and turbine on the site selected
for d in pipeDiameters:
    for z in pipeGrades:
        for y in turbineGrades:
            for x in pumpGrades:
                mwhIn2 = mwh(energyIn(joules(energyOut), pipes[z]['frictionFactor'], siteDictionary[userInput['site']]['performanceRating'], d, siteDictionary[userInput['site']]['angle1'], siteDictionary[userInput['site']]['angle2'],  
                        mass(turbineFlow, waterDensity, fillTime), pumps[x]['efficiency'], turbines[y]['efficiency'], 
                        velocityIn(pumpFlow, d), velocityOut(turbineFlow, d),
                        ))

                # determines the cost of this configuration
                tempCost = (masterCost(
                        x,    siteDictionary[userInput['site']]['performanceRating'], velocityIn(pumpFlow, d), 
                        y, siteDictionary[userInput['site']]['performanceRating'], velocityOut(turbineFlow, d), 
                        siteDictionary[userInput['site']]['angle1'], siteDictionary[userInput['site']]['angle2'], z, d,
                        siteDictionary[userInput['site']]['length'], depth, userInput['site'], reservoirArea(mass(turbineFlow, waterDensity, fillTime), waterDensity)
                        ))

                # if this configuration is within the budget, the Config is updated
                if tempCost <= userInput['budget']:
                    # determines if the efficiency improves with the new grades
                    efficiencyPrint2 = efficiency(energyOut, mwhIn2)
                    if efficiencyPrint2 > efficiencyCheck:
                    # print('In site', userInput['site'], 'the system is', efficiencyPrint2, 'percent efficient and requires', mwhIn2, 'mwh. The cost is', cost)
                        newCost = tempCost
                        currentGrades = x, y, z, efficiencyPrint2, mwhIn2, newCost, d
                    else: 
                        pass
                else:
                    pass

# if there are no possible combinations within the budget, first message is shown
if currentGrades == 0:
    print('There is no possible solution within the specified budget.')

# shows most efficient solution within budget
else:
    print('In site', userInput['site'], 'the system is ', round(currentGrades[3], 0), 'percent efficient and requires', round(currentGrades[4], 0), 'mwh. The cost is', round(currentGrades[5], 0), 'dollars; the cost efficiency is', round(costEfficiency(currentGrades[5], currentGrades[3]), 0), 'dollars per kwh.')
    print('This configuration uses a', currentGrades[0], 'pump, a', currentGrades[1], 'turbine, and', currentGrades[2], 'grade', currentGrades[6], 'meter diameter pipe.')

