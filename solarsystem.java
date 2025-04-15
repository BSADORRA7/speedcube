/**
 * Arctangent. 
 * 
 * Move the mouse to change the direction of the eyes. 
 * The atan2() function computes the angle from each eye 
 * to the cursor. 
 */
 
 // scale factor = 1.388085599
Planet Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune;

float zoom = 1.0;
float theta;
float theta_vel;

void setup() {
  fullScreen();

  Sun = new Planet(0.0, 0.0, 109.00, 255, 255, 0);
  Mercury = new Planet(0.0, 54.890, 0.387, 102, 97, 97);
  Venus = new Planet(0.0, 0.720 + 54.5, 0.722, 199, 168, 90);
  Earth = new Planet(0.0, 1.0 + 54.5, 1.0, 48, 54, 240);
  Mars = new Planet(0.0, 1.52 + 54.5, 1.52, 168, 116, 98);
  Jupiter = new Planet(0.0, 5.20 + 54.5, 5.20, 240, 218, 158);
  Saturn = new Planet(0.0, 9.540 + 54.5, 9.58, 148, 133, 90);
  Uranus = new Planet(0.0, 19.220 + 54.5, 19.20, 116, 200, 252);
  Neptune = new Planet(0.0, 30.06 + 54.5, 30.10, 2, 6, 242);

  Mercury.v = 0.0474;
  Venus.v = 0.035;
  Earth.v = 0.0298;
  Mars.v = 0.0241;
  Jupiter.v = 0.0131;
  Saturn.v = 0.0097;
  Uranus.v = 0.0068;
  Neptune.v = 0.0054;
}

void draw() {
  background(0);

  translate(width/2, height/2);

  Sun.display();
  Mercury.display();
  Venus.display();
  Earth.display();
  Mars.display();
  Jupiter.display();
  Saturn.display();
  Uranus.display();
  Neptune.display();
  
  Sun.updateSize();
  Mercury.updateSize();
  Venus.updateSize();
  Earth.updateSize();
  Mars.updateSize();
  Jupiter.updateSize();
  Saturn.updateSize();
  Uranus.updateSize();
  Neptune.updateSize();

  Mercury.spin();
  Venus.spin();
  Earth.spin();
  Mars.spin();
  Jupiter.spin();
  Saturn.spin();
  Uranus.spin();
  Neptune.spin();
}

void mouseWheel(MouseEvent event) {
  int i = event.getCount();
  if (zoom > 1) {
    if (i > 0) {
      zoom += 0.00005;
      i = 0;
    }
    else {
      zoom -= 0.00005;
      i = 0;
    }
  }
  else {
    zoom += 0.00005;
  }
  Mercury.move();
  Venus.move();
  Earth.move();
  Mars.move();
  Jupiter.move();
  Saturn.move();
  Uranus.move();
  Neptune.move();
}

class Planet {
  float x, y, s, v, ra;
  int r, g, b;
  float theta = 0.0;

  Planet(float a, float b2, float c, int d, int e, int f) {
    x = a;
    y = b2;
    s = c;
    r = d;
    g = e;
    b = f;
    ra = b2;
  }

  void display() {
    noStroke();
    fill(r, g, b);
    circle(x, y, s);
  }
  
  void updateSize() {
    s *= zoom;
  }
  
  void move() {
    x = x * zoom;
    y = y * zoom;
  }

   void spin() {
      y = ra * cos(theta);
      x = ra * sin(theta);

      theta += v;
    }
}
