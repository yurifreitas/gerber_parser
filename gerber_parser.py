def parse_gerber(path, scale=0.01):
    paths = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('X') and 'D' in line:
                x = int(line.split('Y')[0][1:]) * scale
                y = int(line.split('Y')[1].split('D')[0]) * scale
                d = line.split('D')[1].replace('*', '')
                estado = 'move' if d == '02' else 'draw'
                paths.append((x, y, estado))
    return paths
