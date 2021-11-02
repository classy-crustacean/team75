import math


# monkey code dictionaries
pumpGrades    = ('cheap', 'value', 'standard', 'high-grade', 'premium')
turbineGrades = ('meh', 'good', 'fine', 'superb', 'mondo')
pipeGrades    = ('salvage', 'questionable', 'better', 'nice', 'outstanding', 'glorious')
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
    'salvage'      :{'frictionFactor':.05 , 0.10:1.00, .25:1.20, .50:2.57, .75:6.30, 1.00:14, 1.25:26, 1.50:43 , 1.75:68 , 2.00:102, 2.25:144, 2.50:197, 2.75:262, 3.00:340},
    'questionable' :{'frictionFactor':.03 , 0.10:1.20, .25:1.44, .50:3.08, .75:7.56, 1.00:16, 1.25:31, 1.50:52 , 1.75:82 , 2.00:122, 2.25:173, 2.50:237, 2.75:315, 3.00:408},
    'better'       :{'frictionFactor':.02 , 0.10:1.44, .25:1.72, .50:3.70, .75:9.07, 1.00:20, 1.25:37, 1.50:63 , 1.75:98 , 2.00:146, 2.25:208, 2.50:284, 2.75:378, 3.00:490},
    'nice'         :{'frictionFactor':.01 , 0.10:2.16, .25:2.58, .50:5.55, .75:14.0, 1.00:29, 1.25:55, 1.50:94 , 1.75:148, 2.00:219, 2.25:311, 2.50:426, 2.75:567, 3.00:735},
    'outstanding'  :{'frictionFactor':.005, 0.10:2.70, .25:3.32, .50:6.94, .75:17.0, 1.00:37, 1.25:69, 1.50:117, 1.75:185, 2.00:274, 2.25:389, 2.50:533, 2.75:708, 3.00:919},
    'glorious'     :{'frictionFactor':.002, 0.10:2.97, .25:3.55, .50:7.64, .75:19.0, 1.00:40, 1.25:76, 1.50:129, 1.75:203, 2.00:302, 2.25:428, 2.50:586, 2.75:779, 3.00:1011}
    }

siteDictionary = {
    1:{'length':67.8, 'performanceRating':80,  'angle1':30, 'angle2':30}, 
    3:{'length':129,  'performanceRating':120, 'angle1':45, 'angle2':45}}


# inputs, hard coded for now
depth = 20 # depth of the reservoir in meters
energyOut = 120 # mwh required
waterDensity  = 1000 # density of water, kg per m^3
fillTime  = 4.58   # time, in hours for both filling and draining
turbineFlow = 30   # turbine volumetric flow
pumpFlow = 65   # pump volumetric flow
turbineEfficiency = .92  # turbine efficiency
pumpEfficiency = .9   # pump efficiency
g  = 9.81 # gravity, for the love of god dont make this an input
pipeFriction = .05 # pipe friction
pipeLength = 75 # total pipe length
pipeDiameter = 2.00 # pipe diameter
bendConstant1 = .15 # bend constant 1
bendConstant2 = .2  # bend constant 2
bendConstant3 = 0 # bend constant 3
currentGrades = 0

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

# joules to mwh
def mwh(joules):
    return joules / (1E6 * 60 * 60)

# mwh to joules
def joules(mwh):
    return mwh * 3.6E9

# hours in time to seconds
def seconds(hours):
    return hours * 60 * 60

# honestly i dont know what this is
def calcEfficiency(Eout, p, t, Qt, Qp, Nt, Np, g, f, L, D, E1, E2):
    print(Eout, p, t, Qt, Qp, Nt, Np, g, f, L, D, E1, E2)

 
    return 

# Joe's magic user inputs
def getUserInput():
    print("""Choices for site:
    1. Zone 1
    3. Zone 3""")
    sitesInput = input("Enter numbers for zones to consider: ")
    site = 0
    if sitesInput.__contains__('1'):
        site = 1
    if sitesInput.__contains__('3'):
        site = 3
    if sitesInput.__contains__('2'):
        print("Site 2 is on a native american burial ground: You will run out of money in legal fees before you finish; you are now on site 3.")
        site = 3
    
    try:
        budget = int(input("What is your budget? (If no budget, just press enter): "))
    except ValueError:
        budget = 10000000 # really big value that will be bigger than any price
    
    return {'site': site, 'budget': budget}

userInput = getUserInput()

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
    return costPerMeter

# site 1 calculations
def site1cost(reservoirArea):
    # costs for land development
    cost = 0
    cost += 40000 # access road
    cost += 100000 # pumphouse
    cost += (reservoirArea * .25) # reservoir area
    cost += 10000 # random testing 
    return cost

# site 3 calculations
def site3cost(reservoirArea):
    # cost of land development
    cost = 0
    cost += 150000 # access road
    cost += 100000 # pumphouse
    cost += (reservoirArea * .3) # reservoir area development
    cost += (reservoirArea * 1.6) # tree replanting
    return cost

# big cost equation
def masterCost(pumpGrade, performanceRatingUp, flowRateUp, turbineGrade, performanceRatingDown, flowRateDown, angle1, angle2,  pipeGrade, diameter, length, depth, site, area):
    totalCost = 0
    totalCost += pumpCost(pumpGrade, performanceRatingUp, flowRateUp)
    totalCost += turbineCost(turbineGrade, performanceRatingDown, flowRateDown)
    totalCost += fittingCost(angle1, diameter)
    totalCost += fittingCost(angle2, diameter)
    totalCost += pipeCost(pipeGrade, diameter, (siteDictionary[site]['length'] + depth))
    totalCost += wallCost(area, depth)
    
    if site == 1:
        totalCost += site1cost(reservoirArea(mass(turbineFlow, waterDensity, fillTime), waterDensity))
    else:
        totalCost += site3cost(reservoirArea(mass(turbineFlow, waterDensity, fillTime), waterDensity))
    return totalCost
 

# running big equation
efficiencyCheck = 0
currentGrades1 = 0
# for loop site 1
for z in pipeGrades:
    for y in turbineGrades:
        for x in pumpGrades:
            mwhIn2 = mwh(energyIn(joules(energyOut), pipes[z]['frictionFactor'], siteDictionary[1]['performanceRating'], pipeDiameter, siteDictionary[1]['angle1'], siteDictionary[1]['angle2'],  
                    mass(turbineFlow, waterDensity, fillTime), pumps[x]['efficiency'], turbines[y]['efficiency'], 
                    velocityIn(pumpFlow, pipeDiameter), velocityOut(turbineFlow, pipeDiameter),
                    ))
            # determines if it is within budget
            tempCost = (masterCost(
                    x,    siteDictionary[1]['performanceRating'], velocityIn(pumpFlow, pipeDiameter), 
                    y, siteDictionary[1]['performanceRating'], velocityOut(turbineFlow, pipeDiameter), 
                    siteDictionary[1]['angle1'], siteDictionary[1]['angle2'], z, pipeDiameter,
                    siteDictionary[1]['length'], depth, 1, reservoirArea(mass(turbineFlow, waterDensity, fillTime), waterDensity)
                     ))
            if tempCost <= userInput['budget']:
                # determines if the efficiency improves with the new grades
                efficiencyPrint2 = efficiency(energyOut, mwhIn2)
                if efficiencyPrint2 > efficiencyCheck:
                # print('In site', userInput['site'], 'the system is', efficiencyPrint2, 'percent efficient and requires', mwhIn2, 'mwh. The cost is', cost)
                    newCost = tempCost
                    currentGrades1 = x, y, z, efficiencyPrint2, mwhIn2, newCost, 1
                else: 
                    pass
            else:
                pass
# for loop site 3
efficiencyCheck = 0
currentGrades3 = 0
for z in pipeGrades:
    for y in turbineGrades:
        for x in pumpGrades:
            mwhIn2 = mwh(energyIn(joules(energyOut), pipes[z]['frictionFactor'], siteDictionary[3]['performanceRating'], pipeDiameter, siteDictionary[3]['angle1'], siteDictionary[3]['angle2'],  
                    mass(turbineFlow, waterDensity, fillTime), pumps[x]['efficiency'], turbines[y]['efficiency'], 
                    velocityIn(pumpFlow, pipeDiameter), velocityOut(turbineFlow, pipeDiameter),
                    ))
            # determines if it is within budget
            tempCost = (masterCost(
                    x,    siteDictionary[3]['performanceRating'], velocityIn(pumpFlow, pipeDiameter), 
                    y, siteDictionary[3]['performanceRating'], velocityOut(turbineFlow, pipeDiameter), 
                    siteDictionary[3]['angle1'], siteDictionary[3]['angle2'], z, pipeDiameter,
                    siteDictionary[3]['length'], depth, 3, reservoirArea(mass(turbineFlow, waterDensity, fillTime), waterDensity)
                     ))
            if tempCost <= userInput['budget']:
                # determines if the efficiency improves with the new grades
                efficiencyPrint2 = efficiency(energyOut, mwhIn2)
                if efficiencyPrint2 > efficiencyCheck:
                # print('In site', userInput['site'], 'the system is', efficiencyPrint2, 'percent efficient and requires', mwhIn2, 'mwh. The cost is', cost)
                    newCost = tempCost
                    currentGrades3 = x, y, z, efficiencyPrint2, mwhIn2, newCost, 3
                else: 
                    pass
            else:
                pass

# determining response based on user input
if currentGrades1 and currentGrades3 == 0:
    print('There is no possible solution within the specified budget.')
else:
    if userInput['site'] == 1:
        currentGradesAll = currentGrades1
    elif userInput['site'] == 3:
        currentGradesAll = currentGrades3
    else:
        if currentGrades3[3] > currentGrades1[3]:
            currentGradesAll = currentGrades3
        else:
            currentGradesAll = currentGrades1

    print('The most efficient site is site', currentGradesAll[6], ' where the system is ', currentGradesAll[3], 'percent efficient and requires', currentGradesAll[4], 'mwh. The cost is', currentGradesAll[5])