def getCostAndMpg
    cost = 30000  # some fancy db calls go here
    mpg = 30
    return cost,mpg
end
AltimaCost, AltimaMpg = getCostAndMpg
puts "AltimaCost = #{AltimaCost}, AltimaMpg = #{AltimaMpg}"