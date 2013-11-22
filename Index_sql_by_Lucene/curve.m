%polynomial

%curve is more steep while z gets bigger
% z = 0 the f'(x) at 0 and  1 are zero
% z = 1 stright line

z = 0;

a = 2*z-2;
b = 3 - 3*z;
c = z;

x = 0:0.01:1;
y1 = a*x.^3 + b*x.^2 + c*x;

plot(x,y1);


%sin
figure;
y2 = 0.5*sin(pi*(x-0.5))+0.5;
plot(x,y2);

%little difference
dis = y1-y2


%f_tu
figure;
%z is f(0.5) , it should be 0.5~1 here
z = 0.7;
b = 4*z -1;
a = 1-b;
y3 = a*x.^2 + b*x;
plot(x,y3);


%f_ao
figure;
%z is f(0.5) , it should be 0~0.5 here
z = 0.3;
b = 4*z -1;
a = 1-b;
y4 = a*x.^2 + b*x;
plot(x,y4);