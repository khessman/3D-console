# @Date:   2020-12-02T08:22:10+01:00
# @Email:  kalle.hessman@gmail.com
# @Filename: models.py
# @Last modified time: 2020-12-03T22:49:35+01:00

size_x,size_y,size_z = 80,50,50
center_x = int(size_x / 2)
center_y = int(size_y / 2)
center_z = int(size_z / 2)
origin=[center_x,center_y,center_z,1]


cube={
    'description':'a cube',
    'x':None,
    'y':None,
    'points':[
        [[center_x-10],[center_y-10],[center_z-10],[1]],
        [[center_x+10],[center_y-10],[center_z-10],[1]],
        [[center_x+10],[center_y+10],[center_z-10],[1]],
        [[center_x-10],[center_y+10],[center_z-10],[1]],
        [[center_x-10],[center_y-10],[center_z+10],[1]],
        [[center_x+10],[center_y-10],[center_z+10],[1]],
        [[center_x+10],[center_y+10],[center_z+10],[1]],
        [[center_x-10],[center_y+10],[center_z+10],[1]]
    ],
    'lines':[
        [0,1,(255,0,0)],[1,2,(255,0,0)],[2,3,(255,0,0)],[3,0,(255,0,0)],
        [4,5,(0,0,255)],[5,6,(0,0,255)],[6,7,(0,0,255)],[7,4,(0,0,255)],
        [0,4,(0,255,255)],[1,5,(0,255,255)],[2,6,(0,255,255)],[3,7,(0,255,255)]
    ]
}

tree={
    'description':'xmas tree',
    'x':None,
    'y':None,
    'points':[
        [[center_x-10],[center_y-10],[center_z],[1]],
        [[center_x+10],[center_y-10],[center_z],[1]],
        [[center_x],[center_y],[center_z],[1]],

        [[center_x-9],[center_y-9],[center_z+1],[1]],
        [[center_x+9],[center_y-9],[center_z+1],[1]],
        [[center_x],[center_y-1],[center_z+1],[1]],

        [[center_x-8],[center_y-8],[center_z+2],[1]],
        [[center_x+8],[center_y-8],[center_z+2],[1]],
        [[center_x],[center_y-2],[center_z+2],[1]],

        [[center_x-7],[center_y-7],[center_z+3],[1]],
        [[center_x+7],[center_y-7],[center_z+3],[1]],
        [[center_x],[center_y-3],[center_z+3],[1]],

        [[center_x-6],[center_y-6],[center_z+4],[1]],
        [[center_x+6],[center_y-6],[center_z+4],[1]],
        [[center_x],[center_y-4],[center_z+4],[1]],

        [[center_x-5],[center_y-5],[center_z+5],[1]],
        [[center_x+5],[center_y-5],[center_z+5],[1]],
        [[center_x],[center_y-5],[center_z+5],[1]],

        [[center_x-4],[center_y-4],[center_z+6],[1]],
        [[center_x+4],[center_y-4],[center_z+6],[1]],
        [[center_x],[center_y-6],[center_z+6],[1]],

        [[center_x-3],[center_y-3],[center_z+7],[1]],
        [[center_x+3],[center_y-3],[center_z+7],[1]],
        [[center_x],[center_y-7],[center_z+7],[1]],

        [[center_x-2],[center_y-2],[center_z+8],[1]],
        [[center_x+2],[center_y-2],[center_z+8],[1]],
        [[center_x],[center_y-8],[center_z+8],[1]],

        [[center_x-1],[center_y-1],[center_z+9],[1]],
        [[center_x+1],[center_y-1],[center_z+9],[1]],
        [[center_x],[center_y-9],[center_z+9],[1]],
    ],
    'lines':[
        [0,1,(0,255,0)],[1,2,(0,255,0)],[2,0,(0,255,0)],
        [3,4,(0,255,0)],[4,5,(0,255,0)],[5,3,(0,255,0)],
        [6,7,(0,255,0)],[7,8,(0,255,0)],[8,6,(0,255,0)],
        [9,10,(0,255,0)],[10,11,(0,255,0)],[11,9,(0,255,0)],
        [12,13,(0,255,0)],[13,14,(0,255,0)],[14,12,(0,255,0)],
        [15,16,(0,255,0)],[16,17,(0,255,0)],[17,15,(0,255,0)],
        [18,19,(0,255,0)],[19,20,(0,255,0)],[20,18,(0,255,0)],
        [21,22,(0,255,0)],[22,23,(0,255,0)],[23,21,(0,255,0)],
        [24,25,(0,255,0)],[25,26,(0,255,0)],[26,24,(0,255,0)],
        [27,28,(0,255,0)],[28,29,(0,255,0)],[29,27,(0,255,0)],
    ]
}
