class NetworkNode{
    constructor() {
        this.colour = "#000000";
    }
}
class Tank extends NetworkNode{
    constructor() {
        super();
        this.colour = "#7fed18"
    }
}
class Junction extends NetworkNode{
    constructor() {
        super();
        this.colour = "#186aed"
    }
}
class Reservoir extends NetworkNode{
    constructor() {
        super();
        this.colour = "#db6516"
    }
}
class Pump extends NetworkNode{
    constructor() {
        super();
        this.colour = "#cc2727"
    }
}
class CVPipe extends NetworkNode{
    constructor() {
        super();
        this.colour = "#07f59a"
    }
}
class PRV extends NetworkNode{
    constructor() {
        super();
        this.colour = "#a0e009"
    }
}
class PSV extends NetworkNode{
    constructor() {
        super();
        this.colour = "#bd34eb"
    }
}
class PBV extends NetworkNode{
    constructor() {
        super();
        this.colour = "#659e70"
    }
}
class FCV extends NetworkNode{
    constructor() {
        super();
        this.colour = "#2fb598"
    }
}
class TCV extends NetworkNode{
    constructor() {
        super();
        this.colour = "#2facb5"
    }
}
class GPV extends NetworkNode{
    constructor() {
        super();
        this.colour = "#2f4ab5"
    }
}
class NodeFactory{
    constructor() {
        this.tank = null;
        this.junction = null;
        this.reservoir = null;
        this.pump = null;
        this.cVPipe = null;
        this.prv = null;
        this.psv = null;
        this.defaultNode = null;
    }

    getNodeInstance(type) {
        let netNode;
        switch (type) {
            case "Tank":
                netNode = this.tank == null ? new Tank(): this.tank;
                break;
            case "Junction":
                netNode = this.junction == null ? new Junction(): this.junction;
                break;
            case "Reservoir":
                netNode = this.reservoir == null ? new Reservoir(): this.reservoir;
                break;
            case "Pump":
                netNode = this.pump == null ? new Pump(): this.pump
                break;
            case "CVPipe":
                netNode = this.cVPipe == null ? new CVPipe(): this.cVPipe;
                break;
            case "PRV":
                netNode = this.prv == null ? new PRV(): this.prv
                break;
            case "PSV":
                netNode = this.psv == null ? new PSV(): this.psv
                break;
            default:
                netNode = this.defaultNode == null ? new NetworkNode(): this.defaultNode;
                break;
        }
        return netNode;
    }
}
function createGraph(jsonData) {
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 40},
        width = 900 - margin.left - margin.right,
        height = 800 - margin.top - margin.bottom;

// append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Initialize the links
    var link = svg
        .selectAll("line")
        .data(jsonData.links)
        .enter()
        .append("line")
        .style("stroke", "#aaa")

    let nodeFactory = new NodeFactory();
    // Initialize the nodes
    for(let i = 0; i < jsonData.nodes.length; i++) {
        let jsonDataNode = jsonData.nodes[i]
        console.log(jsonDataNode.type)
        let networkNode = nodeFactory.getNodeInstance(jsonDataNode.type)
        svg
            .append("circle")
            .attr("r", 20)
            .style("fill", networkNode.colour)

        svg
            .append("text")
            .attr("font-size", "20px")
            .text(jsonDataNode.id)
    }

    var node = svg
        .selectAll("circle")
        .data(jsonData.nodes)

    var text = svg
        .selectAll("text")
        .data(jsonData.nodes)


    // Let's list the force we wanna apply on the network
    var simulation = d3.forceSimulation(jsonData.nodes)                 // Force algorithm is applied to data.nodes
        .force("link", d3.forceLink()                               // This force provides links between nodes
            .id(function (d) {
                return d.id;
            })                     // This provide  the id of a node
            .links(jsonData.links)                                    // and this the list of links
        )
        .force("charge", d3.forceManyBody().strength(-100))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
        .force("center", d3.forceCenter(width / 2, height / 2))     // This force attracts nodes to the center of the svg area
        .on("end", ticked);

    // This function is run at each iteration of the force algorithm, updating the nodes position.
    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("cx", function (d) {
                return d.x + 6;
            })
            .attr("cy", function (d) {
                return d.y - 6;
            });
        text
            .attr("x", function (d) {
                return d.x + 6;
            })
            .attr("y", function (d) {
                return d.y - 6;
            });
    }


}
