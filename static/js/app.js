let currentGraphData = null;
let selectedNodes = [];

function generateGraph() {
    const numNodes = document.getElementById('num-nodes').value;
    const numEdges = document.getElementById('num-edges').value;
    const graphType = document.getElementById('graph-type').value;
    const isDirected = document.getElementById('directed').checked;

    fetch('/generate_graph', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            num_nodes: parseInt(numNodes, 10),
            num_edges: parseInt(numEdges, 10),
            graph_type: graphType,
            directed: isDirected,
        })
    }).then(response => response.json())
    .then(data => {
        console.log('Received graph data:', data);
        if (!data.elements || !data.elements.nodes || !data.elements.edges) {
            throw new Error('Invalid graph data structure');
        }
        currentGraphData = data.elements;
        renderGraph(data.elements, isDirected);
        refreshSelection(); // Clear node selection after generating a new graph
    }).catch(error => console.error('Error generating graph:', error));
}

function renderGraph(graphElements, isDirected, paths = []) {
    d3.select('#graph-container').selectAll('svg').remove();

    const nodes = graphElements.nodes.map(node => ({ id: node.data.id }));
    const links = graphElements.edges.map(edge => ({
        source: edge.data.source.toString(),
        target: edge.data.target.toString(),
        weight: edge.data.weight
    }));

    const svg = d3.select('#graph-container').append('svg')
        .attr('width', 800)
        .attr('height', 600);

    if (isDirected) {
        svg.append('defs').append('marker')
            .attr('id', 'arrowhead')
            .attr('viewBox', '-0 -5 10 10')
            .attr('refX', 13)
            .attr('refY', 0)
            .attr('orient', 'auto')
            .attr('markerWidth', 13)
            .attr('markerHeight', 13)
            .attr('xoverflow', 'visible')
            .append('svg:path')
            .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
            .attr('fill', '#aaa')
            .style('stroke','none');
    }

    const pathSet = new Set(paths.flat().map(d => d.toString()));

    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(100).strength(1))
        .force("charge", d3.forceManyBody().strength(-500))
        .force("center", d3.forceCenter(svg.attr('width') / 2, svg.attr('height') / 2))
        .force("collide", d3.forceCollide().radius(50));

    const link = svg.selectAll(".link")
        .data(links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke", d => pathSet.has(d.source) && pathSet.has(d.target) ? '#ff0000' : '#aaa')
        .attr('marker-end', d => isDirected ? 'url(#arrowhead)' : '');

    const node = svg.selectAll(".node")
        .data(nodes)
        .enter().append("g")
        .attr("class", "node")
        .attr("id", d => `node-${d.id}`)
        .on("click", function(event, d) {
            nodeClicked(d.id);
        });

    node.append("circle")
        .attr("r", 5)
        .style("fill", d => pathSet.has(d.id) ? '#ff0000' : '#69b3a2');

    node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(d => d.id);

    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
           .attr("transform", d => `translate(${d.x},${d.y})`);
    });
}

function findPath() {
    if (selectedNodes.length < 2) {
        alert('Please select at least two nodes.');
        return;
    }
    const algorithm = document.getElementById('algorithm-select').value;
    const promises = [];

    for (let i = 0; i < selectedNodes.length - 1; i++) {
        promises.push(fetch('/find_path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_node: selectedNodes[i],
                end_node: selectedNodes[i + 1],
                algorithm: algorithm
            })
        }).then(response => response.json()));
    }

    Promise.all(promises)
        .then(results => {
            const paths = results.map(result => result.Route);
            const combinedPath = [].concat(...paths);
            const uniquePath = Array.from(new Set(combinedPath));

            document.getElementById('path-result').textContent = results.map(result => 
                `Path: ${result.Route.join(' -> ')}\nComputation Time: ${result.ComputationTime}ms\nNodes Visited: ${result.NodesVisited}\nTotal Distance: ${result.TotalDistance}\n\n`
            ).join('');
            renderGraph(currentGraphData, document.getElementById('directed').checked, uniquePath);
        })
        .catch(error => console.error('Error finding path:', error));
}

function nodeClicked(nodeId) {
    if (selectedNodes.includes(nodeId)) {
        selectedNodes = selectedNodes.filter(id => id !== nodeId);
    } else {
        selectedNodes.push(nodeId);
    }
    updateSelectedNodesDisplay();
}

function refreshSelection() {
    selectedNodes = [];
    updateSelectedNodesDisplay();
}

function updateSelectedNodesDisplay() {
    document.getElementById('selected-nodes').textContent = `Selected Nodes: ${selectedNodes.join(', ')}`;
}
