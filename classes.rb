class String
    def NullOrEmpty?
    (self == nil || self == "")
    end
end
puts "test".NullOrEmpty?
puts "".NullOrEmpty?