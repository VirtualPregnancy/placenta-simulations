import numpy as np

def read_network(exnode, exelem, term_exnode, radius=None, pressure=None, flow=None):
    #read network from ABI format
    
    #read in nodes
    nfile = open(exnode)
    nsr = nfile.readlines()
    
    #each node is a 3d position vector, guess initial number of nodes by filesize
    nodes = np.zeros((3,int(len(nsr)/4)))
    i = 0
    k = 0
    while i < len(nsr):
        if 'Node:' in nsr[i]:
            #read in x,y,z parts
            for j in np.arange(3):
                nodes[j,k] = float(nsr[i+j+1])
            i += 3
            k += 1
        i += 1
    #delete node entries not used
    nodes = np.delete(nodes,np.arange(k,int(len(nsr)/4)),1)
    nfile.close()
    
    
    #read in edge file
    efile = open(exelem)
    esr = efile.readlines()
    elems = np.zeros((2,int(len(esr)/4)),dtype=int)
    i = 0
    k = 0
    while i < len(esr):
        #parse nodes in and out for edge
        if 'Nodes:' in esr[i]:
            i += 1
            nn = esr[i].split()
            elems[0,k] = int(nn[0])-1
            elems[1,k] = int(nn[1])-1
            k += 1
        i += 1
    elems = np.delete(elems,np.arange(k,int(len(esr)/4)),1)
    efile.close()
    
    
    #read in termnodes -- each entry is a node representing a terminal villous
    tfile = open(term_exnode)
    tsr = tfile.readlines()
    term_nodes = np.zeros(int(len(tsr)/4),dtype=int)
    i = 0
    k = 0
    while i < len(tsr):
        if 'Node:' in tsr[i]:
            ls = tsr[i].split()
            term_nodes[k] = int(ls[1])-1
            i += 3
            k += 1
        i += 1
    term_nodes = np.delete(term_nodes,np.arange(k,int(len(tsr)/4)),0)
    tfile.close()

    
    #find edges in and out of each node
    edges_in = np.zeros(nodes.shape[1],dtype=object)
    edges_out = np.zeros(nodes.shape[1],dtype=object)
    for i in np.arange(len(edges_in)):
        edges_in[i] = np.array([],dtype=int)
        edges_out[i] = np.array([],dtype=int)
    for i in np.arange(elems.shape[1]):
        node = elems[1,i]
        edges_in[node] = np.append(edges_in[node],i)
        node = elems[0,i]
        edges_out[node] = np.append(edges_out[node],i)
        
    #count number of edges in an out of each node
    n_edges_in = np.zeros(nodes.shape[1],dtype=int)
    n_edges_out = np.zeros(nodes.shape[1],dtype=int)
    for i in np.arange(len(n_edges_in)):
        n_edges_in[i] = len(edges_in[i])
        n_edges_out[i] = len(edges_out[i])
    
    nn = np.arange(nodes.shape[1])
    #collect entry (those with no edges in) and exit nodes (those with no edges out)
    entry_nodes = nn[n_edges_in==0]
    exit_nodes = nn[n_edges_out==0]
    
    #read in (edge) radii -- if file has been given
    elem_rads = np.zeros(elems.shape[1])
    if radius != None:
        rfile = open(radius)
        rsr = rfile.readlines()
        i = 0
        k = 0
        while i < len(rsr):
            if 'Values:' in rsr[i]:
                i += 1
                rr = rsr[i].split()
                elem_rads[k] = 0.5*(float(rr[0]) + float(rr[1]))
                k += 1
            i += 1
        rfile.close()
        
    #read in (node) pressurs -- if file has been given
    node_press = np.zeros(nodes.shape[1])
    if pressure != None:
        pfile = open(pressure)
        psr = pfile.readlines()
        i = 0
        k = 0
        while i < len(psr):
            if 'Node:' in psr[i]:
                i += 1
                node_press[k] = float(psr[i])
                k += 1
            i += 1
        pfile.close()
    
    #read in (edge) flow -- if file has been given
    elem_flows = np.zeros(elems.shape[1])
    if flow != None:
        ffile = open(flow)
        fsr = ffile.readlines()
        i = 0
        k = 0
        while i < len(fsr):
            if 'Values:' in fsr[i]:
                i += 1
                ff = fsr[i].split()
                elem_flows[k] = 0.5*(float(ff[0]) + float(ff[1]))
                k += 1
            i += 1
        ffile.close()
    
    
    #return all tree information in the form of a dict
    return {"Nodes": nodes, "Edges": elems, "Term_nodes": term_nodes,\
            "Edges_in": edges_in, "Edges_out": edges_out, "N_edges_in": n_edges_in,\
            "N_edges_out": n_edges_out, "Entry_nodes": entry_nodes, \
            "Exit_nodes": exit_nodes, "Radius": elem_rads, "Pressure": node_press,\
            "Flows": elem_flows}
    
    
def create_tree_vtk(filehead, network, *, NodeData = np.array([]), EdgeData = np.array([]), TermData = np.array([]),
                  NodeNames = np.array([]), EdgeNames = np.array([]), TermNames = np.array([])):
    #output network (dict format) into .vtk format
    #produces two files "filehead_tree.vtk" (a network of edges and nodes)
    #               and "filehead_term.vtk" (terminal nodes containing terminal properties)
    
    filename = ("%s_tree.vtk"%filehead)
    f  = open(filename,'w')
    #write vtk legacy header
    f.write("# vtk DataFile Version 2.0\nTree data %s\nASCII\nDATASET UNSTRUCTURED_GRID\n\n"%filehead)

    Npts = len(network['Nodes'][0])
    f.write("POINTS %d float\n"%Npts)
    for k in np.arange(Npts):
        f.write("%f %f %f\n"%(network['Nodes'][0][k],network['Nodes'][1][k],network['Nodes'][2][k]))
        
    Nedges = len(network['Edges'][0])
    f.write("\nCELLS %d %d\n" % (Nedges,3*Nedges))
    for j in np.arange(Nedges):
        f.write("2 %d %d\n" % (network['Edges'][0][j],network['Edges'][1][j]))
    
    f.write("\nCELL_TYPES %d\n" % (Nedges))
    for j in np.arange(Nedges):
        f.write("3\n")
    
    f.write("\nPOINT_DATA %d\n" % (Npts))
    f.write("\nSCALARS Pressure float\nLOOKUP_TABLE default\n")
    for k in np.arange(Npts):
        f.write("%f\n"%network['Pressure'][k])
    
    #extra node data (if given) is printed here
    if len(NodeData) > 0:
        if len(np.shape(NodeData)) > 1:
            ncols = np.shape(NodeData)[1]
        else:
            ncols = 1
            NodeData = np.reshape(NodeData,(np.shape(NodeData)[0],1))
        for nc in np.arange(ncols):
            f.write("\nSCALARS ")
            if len(NodeNames) > nc:
                f.write("%s "%NodeNames[nc])
            else:
                f.write("NodeData%d "%nc)
            f.write("float\nLOOKUP_TABLE default\n")
            for k in np.arange(Npts):
                f.write("%f\n"%NodeData[k,nc])
    
    f.write("\nCELL_DATA %d\n" % (Nedges))
    f.write("\nSCALARS Flux float\nLOOKUP_TABLE default\n")
    for j in np.arange(Nedges):
        f.write("%f\n"%network['Flows'][j])
        
    f.write("\nSCALARS Radius float\nLOOKUP_TABLE default\n")
    for j in np.arange(Nedges):
        f.write("%f\n"%network['Radius'][j])
    
    #extra edge data (if given) is printed here
    if len(EdgeData) > 0:
        if len(np.shape(EdgeData)) > 1:
            ncols = np.shape(EdgeData)[1]
        else:
            ncols = 1
            EdgeData = np.reshape(EdgeData,(np.shape(EdgeData)[0],1))
        for nc in np.arange(ncols):
            f.write("\nSCALARS ")
            if len(EdgeNames) > nc:
                f.write("%s "%EdgeNames[nc])
            else:
                f.write("EdgeData%d "%nc)
            f.write("float\nLOOKUP_TABLE default\n")
            for k in np.arange(Nedges):
                f.write("%f\n"%EdgeData[k,nc])
                
    f.close()
    
    #terminal nodes file
    filenamet = ("%s_term.vtk"%filehead)
    ft = open(filenamet,'w')
    ft.write("# vtk DataFile Version 2.0\nTerm data %s\nASCII\nDATASET UNSTRUCTURED_GRID\n\n"%filehead)
    Ntnodes = len(network['Term_nodes'])
    ft.write("POINTS %d float\n"%Ntnodes)
    for k in network['Term_nodes']:
        ft.write("%f %f %f\n"%(network['Nodes'][0][k],network['Nodes'][1][k],network['Nodes'][2][k]))
    
    
    ft.write("\nPOINT_DATA %d\n" % (Ntnodes))
    ft.write("\nSCALARS Pressure float\nLOOKUP_TABLE default\n")
    for k in network['Term_nodes']:
        ft.write("%f\n"%network['Pressure'][k])
    
    #extra data (if given) for terminal nodes
    if len(TermData) > 0:
        if len(np.shape(TermData)) > 1:
            ncols = np.shape(TermData)[1]
        else:
            ncols = 1
            TermData = np.reshape(TermData,(np.shape(TermData)[0],1))
        for nc in np.arange(ncols):
            ft.write("\nSCALARS ")
            if len(TermNames) > nc:
                ft.write("%s "%TermNames[nc])
            else:
                ft.write("TermData%d "%nc)
            ft.write("float\nLOOKUP_TABLE default\n")
            for k in np.arange(Ntnodes):
                ft.write("%f\n"%TermData[k,nc])

    ft.close()


tree_path = 'output/'
node_fname = 'full_tree.exnode'
elem_fname = 'full_tree.exelem'
term_fname = 'terminals.exdata'


networks = []
term_props = []

networks=read_network(tree_path + node_fname, tree_path + elem_fname, tree_path + term_fname)
    
create_tree_vtk('vtk', networks)

