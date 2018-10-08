function buildMetadata(sample) {
    // @TODO: Complete the following function that builds the metadata panel
    d3.json(`/metadata/${sample}`).then(function(data){
        console.log(data);
        // Use `d3.json` to fetch the metadata for a sample
        // Use d3 to select the panel with id of `#sample-metadata`
        var panel = d3.select('#sample-metadata');
        // Use `.html("") to clear any existing metadata
        panel.html("");
        
        // Use `Object.entries` to add each key and value pair to the panel
        Object.entries(data).forEach(([key,value]) => {
            // Hint: Inside the loop, you will need to use d3 to append new
            // tags for each key-value in the metadata.
            panel.append('h6').text(`${key}: ${value}`)
            
            
        });
    });
};

function buildCharts(sample) {
    var url = "/samples/" + sample

    // @TODO: Use `d3.json` to fetch the sample data for the plots
    d3.json(url).then(function(response){
        console.log(response);

        var data = [{
            values: response.sample_values.slice(0,10),
            labels: response.otu_ids.slice(0,10),
            hovertext: response.otu_labels.slice(0,10),
            type: 'pie'
        }];
        
        var layout = {
            height: 500,
            width: 600
        };
        
        Plotly.newPlot('pie', data, layout);


        // @TODO: Build a Bubble Chart using the sample data
        var trace1 = [{
            x: response.otu_ids,
            y: response.sample_values,
            mode: 'markers',
            marker: {
                size: response.sample_values,
                color: response.otu_ids,
                text: response.otu_labels
            }
        }];

        
        var layout = {
            title: 'OTU ID',
            showlegend: false,
            height: 400,
            width: 1000
        };
        
        Plotly.newPlot('bubble', trace1, layout);

        // @TODO: Build a Pie Chart
        // HINT: You will need to use slice() to grab the top 10 sample_values,
        // otu_ids, and labels (10 each).

    }); 
    
    

};

function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");

    // Use the list of sample names to populate the select options
    d3.json("/names").then((sampleNames) => {
        sampleNames.forEach((sample) => {
            selector
                .append("option")
                .text(sample)
                .property("value", sample);
        });

        // Use the first sample from the list to build the initial plots
        const firstSample = sampleNames[0];
        buildCharts(firstSample);
        buildMetadata(firstSample);
    });
}

function optionChanged(newSample) {
    // Fetch new data each time a new sample is selected
    buildCharts(newSample);
    buildMetadata(newSample);
}

// Initialize the dashboard
init();
