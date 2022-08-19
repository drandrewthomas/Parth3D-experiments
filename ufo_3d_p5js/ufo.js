// Space image courtesy of and copyright NASA:
// https://images.nasa.gov/details-GSFC_20171208_Archive_e000282

let can, gscl=1, ufo, ufotex, spacepic;
let ufox=0, ufoy=0, ufoz=0;
let uforotx=0, uforoty=0, uforotz=0, spacerotz=0;
let bouncing = false;
let bvexx, bvecy, bvecz, bang, bdist, bwobble=0;

function preload()
{
  ufo = loadModel('./data/simpleufo.obj');
  ufotex = loadImage('./data/simpleufotexture.png');
  spacepic = loadImage('./data/space.jpg');
}

function setup()
{
  var csz = 600;
  if(windowWidth < 600 || windowHeight < 600)
  {
    csz = windowWidth;
    if(windowHeight < csz) csz = windowHeight;
    gscl = csz / 600;
  }
  can = createCanvas(csz, csz, WEBGL);
  frameRate(30);
}

function draw()
{
  if(bouncing) updatebounce();
  background(200);
  ambientLight(100, 100, 100);
  directionalLight(255, 255, 255, -0.5, 0.5, -1);
  perspective(PI/2, float(width)/float(height), 0.1, 20000);
  scale(gscl);
  drawspace();
  drawufo();
  spacerotz += PI/2000;
  if(spacerotz>2*PI) spacerotz-=2*PI;
  uforotx += PI/80;
  if(uforotx>2*PI) uforotx-=2*PI;
  uforoty += PI/100;
  if(uforoty>2*PI) uforoty-=2*PI;
  if(bwobble > 0.01)
  {
    bwobble *= 0.98;
    uforotz += PI/100;
    if(uforotz>2*PI) uforotz-=2*PI;
  }
  else
  {
    bwobble = 0;
    uforotz = 0;
  }
}

function mousePressed()
{
  var mag;
  if(mouseX>=0 && mouseX<width && mouseY>=0 && mouseY<height)
  {
    if(!bouncing)
    {
      // Make a vector for the bounce
      bvecx = map(mouseX, 0, width, -1, 1);
      bvecy = map(mouseY, 0, height, -1, 1);
      bvecz = 1;
      // Normalize the bounce vector (i.e. mag=0)
      mag = sqrt(bvecx * bvecx + bvecx * bvecz + bvecz * bvecz);
      bvecx /= mag;
      bvecy /= mag;
      bvecz /= mag;
      // Make a random bounce distance and speed
      bdist = (random() * 9000) + 300;
      bspeed = (random() * (PI / 20)) + PI/50;
      // Set start of bounce
      bang = 0;
      bwobble = (random() * 0.5) + 0.5;
      bouncing = true;
    }
  }
  return false;
}

function updatebounce()
{
  if(bang > PI)
  {
    bouncing = false;
    ufox = 0;
    ufoy = 0;
    ufoz = 0;
  }
  else
  {
    bmag = sin(bang) * bdist;
    ufox = -bvecx * sin(bang) * bdist;
    ufoy = -bvecy * sin(bang) * bdist;
    ufoz = -bvecz * sin(bang) * bdist;
    bang += bspeed;
  }
}

function drawufo()
{
  push();
  translate(ufox, ufoy, ufoz - 20);
  scale(300);
  rotateX(-cos(uforotx) * (PI * 0.1) - (PI * 0.075));
  rotateY(uforoty);
  scale(-1, 1, 1);
  rotateZ(-cos(uforotz) * (PI * 0.3) * bwobble);
  rotateZ(PI);
  noStroke();
  texture(ufotex);
  model(ufo);
  pop();
}

function drawspace()
{
  var wid=1041, hgt=987;
  push();
  translate(0, 0, -10000);
  rotateZ(-spacerotz);
  scale(30);
  texture(spacepic);
  beginShape();
  textureMode(NORMAL);
  noStroke();
  vertex(-wid/2, -hgt/2, 0, 0, 0);
  vertex(wid/2, -hgt/2, 0, 1, 0);
  vertex(wid/2, hgt/2, 0, 1, 1);
  vertex(-wid/2, hgt/2, 0, 0, 1);
  endShape();
  pop();
}

