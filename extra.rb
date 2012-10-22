def test(a=1,b=2,*c)
  puts "#{a},#{b}"
  c.each{|x| print " #{x}, "}  # We will learn about "each" very soon.  I promise.
end
test 3, 6, 9, 12, 15, 18