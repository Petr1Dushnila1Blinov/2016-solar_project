# coding: utf-8
# license: GPLv3
import math
from solar_objects import Star, Planet
G = gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5

        if r >= 2*(body.R + obj.R):
            F = (G*body.m*obj.m)/(r**2)
            body.Fx += F*(obj.x-body.x)/r
            body.Fy += F*(obj.y-body.y)/r



def move_space_object(body, dt, space_objects):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """

    ax = body.Fx/body.m
    body.x += body.Vx * dt        # FIXED
    body.Vx += ax*dt
    ay = body.Fy / body.m
    body.y += body.Vy * dt        # FIXED
    body.Vy += ay * dt

    for obj in space_objects:
        r = ((body.x - obj.x) ** 2 + (body.y - obj.y) ** 2) ** 0.5
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!

        if r<= 1.2 * (body.R + obj.R):
            destruction(body, space_objects)
            destruction(obj, space_objects)


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt, space_objects)


def destruction(body, space_objects):
    body.Vx *= 0.8
    body.Vy *= 0.8
    body.R *= 0.5
    body.m *= 0.5
    turn(body, 1)

    newbody = Planet()
    newbody.R = body.R
    newbody.m = body.m
    newbody.x = body.x
    newbody.y = body.y
    newbody.Vx = body.Vx
    newbody.Vy = body.Vy
    newbody.color = body.color


    turn(newbody, -2)

    space_objects.append(newbody)






def turn(body, angle):
    V = (body.Vx ** 2 + body.Vy ** 2) ** 0.5
    if body.Vy >= 0:
        Ang = math.atan(body.Vy / body.Vx)
    else:
        Ang = math.pi + math.atan(body.Vy / body.Vx)
    body.Vx = V * math.cos(Ang+angle)
    body.Vy = V * math.sin(Ang+angle)


if __name__ == "__main__":
    print("This module is not for direct call!")
