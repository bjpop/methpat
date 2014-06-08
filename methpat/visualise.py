import json
import logging

def make_html(args, amplicon_names, json_dict):
    js_strings = []
    for amplicon_name in amplicon_names:
    #for amplicon, amplicon_dict in json_dict.items():
        try:
            amplicon_dict = json_dict[amplicon_name]
        except KeyError:
            logging.info("No methylation patterns found for {}".format(amplicon_name))
            continue
        # sort patterns on count in descending order
        amplicon_dict['patterns'].sort(key=lambda x:x['count'], reverse=True)
        json_str = json.dumps(amplicon_dict)
        js_strings.append('create_matrix({});'.format(json_str))
    doc = DOC_TEMPLATE % '\n'.join(js_strings)
    with open(args.html, 'w') as html_file:
        html_file.write(doc)

DOC_TEMPLATE = '''
<!DOCTYPE html>
<meta charset="utf-8">
<title>Methylation patterns</title>
<style>

.background {
  fill: #eee;
}

line {
  stroke: #fff;
  stroke-opacity: .5;
  shape-rendering: crispEdges;
}

textarea {
  padding: 2px;
  width: 714px;
  height: 360px;
}

.axis path,
.axis line {
    fill: none;
    stroke: black;
    shape-rendering: crispEdges;
}

.axis text {
    font-family: sans-serif;
    font-size: 11px;
}

#settings {
   display:none
}

/*
.meta_data_table {
   margin: 10px;
}
*/

</style>

<h1>Methylation Patterns</h1>

<div id="settings">
<hr>
<h3>Visualisation settings</h3>

<table>
<tr>
   <td>scaling</td>
   <td><select id="histogram_scaling">
      <option value="log">log</option>
      <option value="linear">linear</option>
      </select>
   </td>
</tr>
<tr>
   <td>scale pattern intensity</td>
   <td><select id="scale_pattern_intensity">
      <option value="false">false</option>
      <option value="true">true</option>
      </select>
   </td>
</tr>
</table>

<h4>Pattern sorting</h4>
<table>
<tr><td>sort by</td>
    <td><select id="pattern_sort_by">
      <option value="frequency">epiallele frequency</option>
      <option value="methylation">degree of methylation</option>
      </select>
    </td>
</tr>
<tr><td>sort direction</td>
    <td><select id="pattern_sort_direction">
        <option value="descending">descending</option>
        <option value="ascending">ascending</option>
        </select>
    </td>
</tr>
</table>

<h4>Methylation colours</h4>
<table>
<tr><td>methylated</td><td><input type="color" id="methylated_colour" value="#fffb00"></td></tr>
<tr><td>unmethylated</td><td><input type="color" id="unmethylated_colour" value="#f90000"></td></tr>
<tr><td>unknown</td><td><input type="color" id="unknown_colour" value="#0000f9"></td></tr>
</table>

<h4>Histogram settings</h4>
<table>
<tr>
   <td>visible</td>
   <td><select id="histogram_visible">
      <option value="true">true</option>
      <option value="false">false</option>
      </select>
   </td>
</tr>
<tr>
   <td>units</td>
   <td><select id="histogram_units">
      <option value="percent">percent</option>
      <option value="absolute">absolute</option>
      </select>
   </td>
</tr>
<tr><td>colour</td>
    <td><input type="color" id="histogram_colour" value="#00f900"></td></tr>
</table>
<hr>
</div>
<p>
<input id="toggle_settings" type="button" value="show settings">
</p>
<p>
<input id="redraw" type="button" value="redraw">
</p>

<script type="text/javascript" src="d3.v3.min.js"></script>
<script type="text/javascript" src="jquery-1.6.4.min.js"></script>
<script>

var scaling = 'log';

$('#toggle_settings').click(function () {
   var buttonLabel = $(this).val();
   if (buttonLabel == "show settings") {
      $(this).val("hide settings");
   }
   else {
      $(this).val("show settings");
   }
   $('#settings').toggle();
});


$('#redraw').click(function () {
   draw_graphs();
});

/*
   We encode methylated: 1
             unmethylated: 0
             unknown: 2

   We use this sum for sorting, so we just sum
   the 1s, and not the 0s or 2s.
*/
function sum_methylation(a) {
   var result = 0;
   for(var i = 0; i < a.length; i++){
      if (a[i] == 1) {
         result++;
      }
   }
   return result;
}

function order_pattern(m1, m2, order_by, direction) {
   switch(order_by){
      case "frequency":
         var delta = order_pattern_by_frequency(m1, m2);
         break;
      case "methylation":
         var delta = order_pattern_by_methylation(m1, m2);
         break;
   }

   switch(direction) {
      case "ascending":
         return delta;
         break;
      case "descending":
         return -delta;
         break;
      default:
         return delta;
         break;
   }
}

function order_pattern_by_frequency(m1, m2) {
   return m1.count - m2.count;
}

function order_pattern_by_methylation(m1, m2) {
   var sum1 = sum_methylation(m1.methylation);
   var sum2 = sum_methylation(m2.methylation);

   var delta = sum1 - sum2;

   // If they have the same number of 1s, then sort
   // by their frequency.
   if (delta == 0) {
      delta = m1.count - m2.count;
   }
   return delta;
}

function scale_count(count, total_count, units) {
   switch(units){
      case "percent":
         return count / total_count * 100;
         break;
      case "absolute":
         return count;
         break;
   }
}

function create_matrix(data) {

   var patterns = data.patterns;
   var num_patterns = patterns.length;

   if (num_patterns == 0)
      return;

   var scale_pattern_intensity = $('#scale_pattern_intensity').val()
   var histogram_visible = $('#histogram_visible').val()
   var histogram_colour = $('#histogram_colour').val()
   var methylated_colour = $('#methylated_colour').val()
   var unmethylated_colour = $('#unmethylated_colour').val()
   var unknown_colour = $('#unknown_colour').val()
   var histogram_scaling = $('#histogram_scaling').val();
   var histogram_units = $('#histogram_units').val();
   var pattern_sort_by = $('#pattern_sort_by').val();
   var pattern_sort_direction = $('#pattern_sort_direction').val();

   patterns.sort(function(a, b) { return order_pattern(a, b, pattern_sort_by, pattern_sort_direction); });

   var num_sites = patterns[0].methylation.length

   if (histogram_visible == 'true') {
      var margin = {top: 0, right: 10, bottom: 10, left: 50};
   }
   else
   {
      var margin = {top: 0, right: 10, bottom: 10, left: 10};
   }

   var all_graphs = d3.select("body").select("#all_graphs");

   var this_graph = all_graphs.append("div")
   
   // if we want drag and drop then we need to set:
   // this_grahp.attr("draggable", "true");

   var heading = this_graph.append("h3");
   heading.text(data.amplicon + ' ' + data.chr + ' ' + data.start + ':' + data.end)

   // If we want to display the meta data in a table:
   /*
   var meta_data_table_div = this_graph.append("div");
   var meta_data_table = meta_data_table_div.append("table").attr("class", "meta_data_table").attr("border", "1");
   var heading_row = meta_data_table.append("tr");
   heading_row.append("th").text("amplicon"); 
   heading_row.append("th").text("chrom"); 
   heading_row.append("th").text("start"); 
   heading_row.append("th").text("end"); 
   var data_row = meta_data_table.append("tr");
   data_row.append("td").text(data.amplicon); 
   data_row.append("td").text(data.chr); 
   data_row.append("td").text(data.start); 
   data_row.append("td").text(data.end); 
   */

   // Compute the maximum, minimum and total counts for all the data.
   var max_count = -1, min_count = -1, total_count = 0;
   for (i = 0; i < num_patterns; i++)
   {
      this_count = patterns[i].count;
      total_count += this_count;
      if (min_count == -1 || this_count < min_count)
      {
         min_count = this_count;
      }
      if (max_count == -1 || this_count > max_count)
      {
         max_count = this_count;
      }
   } 

   var cell_width = 10;
   var cell_height = cell_width;
   var width = num_sites * cell_width;

   var patterns_height = num_sites * cell_height;
   var counts_height = 100;
   var horizontal_gap = 10;
   var vertical_gap = 3;

   var img_width = num_patterns * cell_width + margin.left + margin.right + vertical_gap;
   if (histogram_visible == 'true') {
      var img_height = patterns_height + horizontal_gap + counts_height + margin.top + margin.bottom;
   }
   else {
      var img_height = patterns_height + margin.top + margin.bottom;
   }

   var cell_y = d3.scale.ordinal()
      .domain(d3.range(num_sites))
      .rangeBands([0, patterns_height]);

   switch(histogram_units) {
      case 'percent':
         // we use 0.0001 as the lower bound because the log scale does not support 0
         var scale_domain = [0.0001, 100];
         break;
      case 'absolute':
         var scale_domain = [1, max_count];
         break;
   } 

   var mag_range = [0.2, 0.7];
   var histo_range = [1, counts_height];

   switch(histogram_scaling) {
      case 'linear':
         var mag_scaler = d3.scale.linear();
         var histo_scaler = d3.scale.linear();
         break
      case 'log':
         var mag_scaler = d3.scale.log();
         var histo_scaler = d3.scale.log();
         break
   }

   var mag_scale = mag_scaler.domain(scale_domain).range(mag_range);
   var histo_scale = histo_scaler.domain(scale_domain).range(histo_range);

   var patterns_svg = this_graph.append("svg")
      .attr("height", img_height)
      .attr("width", img_width)

   var image_group = patterns_svg.append("g")
      .attr("transform", "translate(" + (margin.left) + "," + 0 + ")");

   var histo_y_axis = d3.svg.axis()
      .scale(histo_scale)
      .orient("left")
      .ticks(5);

   var patterns_group = image_group.append("g")
      .attr("class", "patterns")
      .attr("transform", "translate(" + vertical_gap + "," + 0 + ")");

   var columns = patterns_group.selectAll(".column")
       .data(patterns)
       .enter().append("g")
       .attr("class", "column")
       // translate the column in the x direction (shift it across the page)
       .attr("transform", function(d, i) { return "translate(" + i * cell_width + ",0)"; });

   columns.selectAll(".cell")
       .data(function(d) {
           values = [];
           for (i = 0; i < num_sites; i++)
           {
               var cell_val = { meth_state : d.methylation[i], count : d.count }
               values.push(cell_val);
           }
           return values.reverse();
       })
       .enter().append("rect")
       .attr("class", "cell")
       // shift the row down by the cell height
       .attr("y", function(d, i) { return cell_y(i); })
       .attr("width", cell_width)
       .attr("height", cell_height)
       .attr("stroke-width", 0.5)
       .attr("stroke", 'black')
       .attr("fill", function(d, i) {

           function make_colour(name, count) {
              var colour = d3.hsl(name);
              if (scale_pattern_intensity == 'true') {
                 colour.l = mag_scale(scale_count(count, total_count, histogram_units));
              }
              return colour;
           }

           var meth_state = d.meth_state;

           if (meth_state == 0) {
              return make_colour(unmethylated_colour, d.count);
           }
           else if (meth_state == 1) {
              return make_colour(methylated_colour, d.count);
           } 
           else if (meth_state == 2) {
              return make_colour(unknown_colour, d.count);
           };
        })

    if (histogram_visible == 'true') {
        var histogram = image_group.append("g")
          .attr("class", "histogram");

        var histogram_bars = histogram.append("g")
          .attr("class", "histogram_bars")
          .attr("transform", "translate(" + vertical_gap + "," + 0 + ")");

        var count_bars = histogram_bars.selectAll(".count_bar")
           .data(patterns)
           .enter().append("rect")
           .attr("class", "count_bar")
           .attr("transform", function(d, i)
               { return "translate(" + (i * cell_width) + "," + (patterns_height + horizontal_gap) + ")"; })
           .attr("class", "cell")
           .attr("width", cell_width)
           .attr("height", function(d, i) { return histo_scale(scale_count(d.count, total_count, histogram_units)); })
           .attr("fill", histogram_colour);

        histogram.append("g").
            attr("class", "axis").
            attr("transform", "translate(" + 0 + "," + (patterns_height + horizontal_gap) + ")").
            call(histo_y_axis)
    }
}

function draw_graphs() {

   d3.select("body").select("#all_graphs").remove();

   var all_graphs = d3.select("body")
      .append("div")
      .attr("id", "all_graphs");

   %s
}

draw_graphs();

</script>
'''
