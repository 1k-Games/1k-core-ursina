'''
From Lyfe on Ursina Discord
'mp4 texture at 2k fps'
https://discord.com/channels/593486730187899041/596647535913861120/949611923807297537

NOTE - Use this idea at least, on far away mesh points that are supposed to represent shields. 
- Instead of just being a circle in the distance, it can be a circle with the same type of ripple effect that you'd see on the shields when they are much closer???
- Or can we just straightway use the bubbleshield technique but do it on the shader level in here? 
    - can this be the same as the other technique? Or can we actually use this as a complete, much faster replacement than the other one where we displace the texture with pure python? 
    
'''

from ursina import *

ripple_shader = Shader(language=Shader.GLSL,
vertex='''
#version 140
uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 texcoords;
out vec4 draw_color;
void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoords = p3d_MultiTexCoord0.xy;
    draw_color = vec4(0.5,0.5,1.,1.);
}
''',
fragment='''
#version 140
in vec2 texcoords;
in vec4 draw_color;
out vec4 fragColor;
uniform float shadertime;
void main() {
    float x = (texcoords.x - 0.5);
    float y = (texcoords.y - 0.5);
    float len = sqrt(x*x + y*y);
    vec3 out_color = draw_color.xyz * vec3((sin(len*3.14*10-5*shadertime)*sin(shadertime+len)+1)/2);
    //vec3 out_color = draw_color.xyz * vec3((sin(len*3.14*10-5*shadertime)*sin(shadertime+len)+1)*cos(shadertime+6*len)/2);
    fragColor = vec4(out_color, 1.).rgba;
}
'''
)

class ripple_shaded_entity(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, *args, shader=ripple_shader, **kwargs)

if __name__ == '__main__':
    app = Ursina(vsync=False)
    editor_camera = EditorCamera(enabled=True, ignore_paused=True, rotation=(60,0,0))
    ground = ripple_shaded_entity(model='plane')
    start = time.time()
    def update():
        ground.set_shader_input('shadertime', time.time()-start)
    ground.collider = ground.model
    app.run()