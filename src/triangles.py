from numpy import sqrt

class Particle:
    ''' Moving particles. '''

    def __init__(self, x0, v0, name):

        self.posx = x0[0]
        self.posy = x0[1]
        self.velx = v0[0]
        self.vely = v0[1]
        self.name = str(name)

    def reflect(self, dir='ver'):
        '''
        Reflect particle as if it had collided with either a horizontal (hor) or
        a vertical (ver) wall.
        '''

        if dir == 'ver':
            self.velx *= -1
        elif dir == 'hor':
            self.vely *= -1

    def update_pos(self, step):
        ''' Update particle position after time step. '''

        self.posx += self.velx*step
        self.posy += self.vely*step

    def find_neighbors(self, particles):
        ''' Find the two nearest neighbors. '''

        # Initialize distances of nearest neighbors as infinity
        d1 = d2 = float('inf')
        neighbor1 = neighbor2 = 0

        for p in particles:
            # Find distance between this and another particle
            d = sqrt((self.posx - p.posx)**2 + (self.posy - p.posy)**2)
            # Update neighbors
            if d <= d1 and self != p:
                neighbor1, neighbor2 = p, neighbor1
                d1, d2 = d, d1
            elif d <= d2 and self != p:
                neighbor2 = p
                d2 = d

        return neighbor1, neighbor2

def write(lists, filename):
    ''' Writes several lists to a file, each in a separate column. '''

    with open(filename, 'w') as f:
        row_no = len(lists[0])
        for i in range(row_no):
            line = '{'
            for list in lists[:-1]:
                line += str(list[i]) + '/'
            line += str(lists[len(lists)-1][i])

            if i == row_no -1:
                line += '}\n'
            else:
                line +=  '},\n'

            f.write(line)

def remove_duplicates(tuples):
    '''
    Removes duplicates tuples.

    The tuple (x, y) is considered to be equal to both (x, y) and (y, x).
    '''

    list = []
    for (x, y) in tuples:
        if not (x, y) in list and not (y, x) in list:
            list.append((x, y))

    return list

if __name__ == '__main__':

    from numpy.random import uniform as rnd
    import numpy as np

    # Define animation parameters
    fps = 30
    tf = 15
    N = 80
    speed = 0.3

    # Initialize
    positions = [(rnd(), rnd()) for i in range(N)]
    angles = [rnd(0, 2*np.pi) for i in range(N)]
    speeds = [rnd(0.1, 1)*speed for i in range(N)]
    velocities = [(v*np.cos(angle), v*np.sin(angle)) \
                  for angle, v in zip(angles, speeds)]
    names = [i for i in range(N)]
    particles = [Particle(pos, vel, name) \
                 for pos, vel, name in zip(positions, velocities, names)]

    # Animate
    h = 1/fps
    times = np.arange(0, tf, h)
    for (i, ti) in enumerate(times):
        # Save current positions
        file = '../raw/positions-' + str(i) + '.txt'
        write([[p.posx for p in particles],
               [p.posy for p in particles],
               [p.name for p in particles]],
              file)

        # Find pairs of nearest neighbors
        pairs = []
        for p in particles:
            n1, n2 = p.find_neighbors(particles)
            pairs.append((p, n1))
            # pairs.append((p, n2))

        pairs = remove_duplicates(pairs)

        # Save lines between neighbors
        start_names = [start.name for (start, end) in pairs]
        end_names = [end.name for (start, end) in pairs]
        file = '../raw/connections-' + str(i) + '.txt'
        write([start_names, end_names], file)

        # Reflect velocities if collisions took place (walls have length 1)
        for p in particles:
            if p.posx <= 0 or p.posx >= 1:
                p.reflect('ver')
            elif p.posy <= 0 or p.posy >= 1:
                p.reflect('hor')

        # Update positions
        for p in particles:
            p.update_pos(h)
