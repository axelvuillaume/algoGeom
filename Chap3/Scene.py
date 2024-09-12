class Scene:
    
    def viewportMatrix(sx, sy, hs, ws):
        return [
            [ws/2, 0, 0 ,sx + ws/2],
            [0, hs/2, 0 , sy+hs/2],
            [0,0,1, 0],
            [0,0,0,1],
        ]
        
    def projectionMatrix(l,r,t,b,n,f):
        return [
            [2/(r-l), 0, 0 ,- (r+l)/(r-l)],
            [0, 2/(t-b), 0 , -(t+b)/(t-b)],
            [0,0,-2/(f-n), -(f+n)/(f-n)],
            [0,0,0,1],
        ]