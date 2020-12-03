# @Date:   2020-12-02T08:22:10+01:00
# @Email:  kalle.hessman@gmail.com
# @Filename: models.py
# @Last modified time: 2020-12-02T09:00:27+01:00

size_x,size_y,size_z = 80,50,50
center_x = int(size_x / 2)
center_y = int(size_y / 2)
center_z = int(size_z / 2)
origin=[center_x,center_y,center_z,1]


my_3dmodel={
    'name':'cube',
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
