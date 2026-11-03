"""Inspect the Boolean node sockets before any candidate construction."""
import json,os,sys,bpy

RUN='EXP-BPY-006-GN-DIAG-20261102T190420Z'
def main():
    if '--' not in sys.argv or len(sys.argv[sys.argv.index('--')+1:])!=1: raise RuntimeError('Expected JSON output path after --')
    output=os.path.abspath(sys.argv[sys.argv.index('--')+1])
    tree=bpy.data.node_groups.new('GN_DIAG_API_ONLY','GeometryNodeTree')
    node=tree.nodes.new('GeometryNodeMeshBoolean'); node.operation='UNION'
    inputs=[{'index':i,'name':s.name,'identifier':s.identifier,'type':s.type,'multi_input':s.is_multi_input,'enabled':s.enabled} for i,s in enumerate(node.inputs)]
    outputs=[{'index':i,'name':s.name,'identifier':s.identifier,'type':s.type,'enabled':s.enabled} for i,s in enumerate(node.outputs)]
    geometry=[s for s in node.outputs if s.type=='GEOMETRY' and s.enabled]
    resolved={'name':geometry[0].name,'identifier':geometry[0].identifier,'type':geometry[0].type} if len(geometry)==1 else None
    result={'run_id':RUN,'blender_version':bpy.app.version_string,'operation':'UNION','inputs':inputs,'outputs':outputs,'geometry_output_candidates':[{'name':s.name,'identifier':s.identifier,'type':s.type} for s in geometry],'resolved_geometry_output':resolved,'resolution_unambiguous':len(geometry)==1}
    os.makedirs(os.path.dirname(output),exist_ok=True)
    with open(output,'x',encoding='utf-8') as f: json.dump(result,f,indent=2); f.write('\n')
    print('GN_BOOLEAN_API '+json.dumps(result,sort_keys=True))
    if len(geometry)!=1: raise SystemExit(2)
main()
