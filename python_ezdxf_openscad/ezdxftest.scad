union()
{
  linear_extrude(height = 1.5, center = true, convexity = 10)
    import (file = "ezdxftest.dxf", layer = "outer");
  translate([0, 0, 2.5])
    linear_extrude(height = 5, center = true, convexity = 10)
      import (file = "ezdxftest.dxf", layer = "inner"); 
}
