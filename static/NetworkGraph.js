class NetworkNode{
    constructor() {
        this.colour = null;
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

class NodeFactory{
    constructor() {
        this.reservoir = null;
        this.junction = null;
        this.tank = null;
    }

    getNodeInstance(type) {
        let netNode = null;
        switch (type) {
            case "Junction":
                netNode = this.junction == null ? new Junction(): this.junction;
                break;
            case "Tank":
                netNode = this.tank == null ? new Tank(): this.tank;
                break;
            case "Valve":
                return "#07f59a"
            case "Pipe":
                return "#ccb927"
            case "Pump":
                return "#cc2727"
            case "Reservoir":
                netNode = this.reservoir == null ? new Reservoir(): this.reservoir;
                break;
            default:
                return "#8e07f5"
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
