# Template for the output HTML document
# %s patterns are filled in with computed values.

DOC_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Methylation patterns</title>

<style>

.background {
  fill: #eee;
}

line {
  stroke: #fff;
  stroke-opacity: 0.5;
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

#redraw { margin-top: 10px; margin-bottom: 10px; }
#info_alert { margin-top: 10px; }
</style>

<!-- web assets -->
%s

</head>
<body>

<div class="container-fluid">

    <div class="page-header">
        <h1>%s</h1>
    </div>

    <ul class="nav nav-tabs">
        <li class="nav active"><a href="#Graphs" data-toggle="tab">Graphs</a></li>
        <li class="nav"><a href="#Settings" data-toggle="tab">Settings</a></li>
        <li class="nav"><a href="#Order" data-toggle="tab">Order</a></li>
        <li class="nav"><a href="#Info" data-toggle="tab">Info</a></li>
    </ul>

    <!-- Tab panes -->
    <div class="tab-content">

        <div class="tab-pane active" id="Graphs">
            <button id="redraw" type="button" class="btn btn-primary">Redraw</button>
            <div id="all_graphs"></div>
        </div>

        <div class="tab-pane" id="Order">
            <h3>Amplicon order</h3>
            <div class="row">
               <div class="col-md-3">
                  <p>Drag the amplicon names up or down to reorder their display.</p>
                  <ul id="amplicon_order" class="list-group">
                     <!-- List of amplicon names in sortable list -->
                     %s
                  </ul>
               </div>
            </div>
        </div>

        <div class="tab-pane" id="Settings">

            <h3>Visualisation settings</h3>

            <div class="row">
                <div class="col-md-3">
                    <h4>Methylation patterns</h4>
                    <form role="form">
                        <div class="form-group">
                            <label for="pattern_cell_size">Cell size (pixels)</label>
                            <input id="pattern_cell_size" class="form-control" type="number" min="1" max="9999" value="15">
                        </div>

                        <div class="form-group">
                            <label for="scale_pattern_intensity">Scale pattern intensity</label>
                            <select id="scale_pattern_intensity" class="form-control">
                                <option value="false">false</option>
                                <option value="true">true</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="methylation_site_direction">Methylation site direction</label>
                            <select id="methylation_site_direction" class="form-control">
                                <option value="ascending">ascending</option>
                                <option value="descending">descending</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="pattern_sort_by">Sort methylation patterns by</label>
                            <select id="pattern_sort_by" class="form-control">
                                <option value="frequency">epiallele frequency</option>
                                <option value="methylation">degree of methylation</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="pattern_sort_direction">Sort direction (left to right)</label>
                            <select id="pattern_sort_direction" class="form-control">
                                <option value="descending">descending</option>
                                <option value="ascending">ascending</option>
                            </select>
                        </div> 

                        <div class="form-group">
                            <label for="pattern_read_threshold">Pattern read threshold (percent)</label>
                            <input id="pattern_read_threshold" class="form-control" type="number" min="0" max="100" value="0">
                        </div> 

                        <div class="form-group">
                            <label for="png_save_scale">PNG file save scale factor</label>
                            <input id="png_save_scale" class="form-control" type="number" min="1" value="1">
                        </div> 


                    </form>
                </div> <!-- col -->

                <div class="col-md-3">
                    <h4>Histogram</h4>
                    <form role="form">

                        <div class="form-group">
                            <label for="histogram_scaling">Histogram scaling</label>
                            <select id="histogram_scaling" class="form-control">
                                <option value="linear">linear</option>
                                <option value="log">log</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="histogram_visible">Histogram visible</label>
                            <select id="histogram_visible" class="form-control">
                                <option value="true">true</option>
                                <option value="false">false</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="histogram_height">Histogram height (pixels)</label>
                            <input id="histogram_height" class="form-control" type="number" min="1" max="9999" value="100">
                        </div>

                        <div class="form-group">
                            <label for="histogram_units">Histogram units</label>
                            <select id="histogram_units" class="form-control">
                                <option value="absolute">absolute</option>
                                <option value="percent">percent</option>
                            </select>
                        </div>
                    </form>
                </div> <!-- col -->

                <div class="col-md-2">
                    <h4>Colour</h4>
                    <form role="form">
                        <div class="form-group">
                            <label for="methylated_colour">Methylated site</label>
                            <input type="color" id="methylated_colour" class="form-control" value="#FFFF00">
                        </div> 

                        <div class="form-group">
                            <label for="unmethylated_colour">Unmethylated site</label>
                            <input type="color" id="unmethylated_colour" class="form-control" value="#0000FF">
                        </div> 

                        <div class="form-group">
                            <label for="unknown_colour">Unknown site</label>
                            <input type="color" id="unknown_colour" class="form-control" value="#AAAAAA">
                        </div> 
                        <div class="form-group">
                            <label for="histogram_colour">Histogram</label>
                            <input type="color" id="histogram_colour" class="form-control" value="#797979">
                        </div>
                    </form>
                </div> <!-- col -->
            </div> <!-- row -->
        </div> <!-- pane -->

        <div class="tab-pane" id="Info">
            <div id="info_alert" class="alert alert-info" role="alert">
                Methylation pattern visualisation created with
                <a href="http://bjpop.github.io/methpat/">methpat</a>.
            </div>
        </div>

    </div> <!-- tab content -->
</div> <!-- container -->
                
<script>

var amplicon_names = [];
var scaling = 'log';

$('#redraw').click(function () {
   draw_graphs();
});

$("#amplicon_order").sortable();
$("#amplicon_order").disableSelection();

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

   var unique_id = data.unique_id;
   var patterns = data.patterns;
   var num_patterns = patterns.length;

   if (num_patterns == 0)
      return;

   var histogram_height = parseInt($('#histogram_height').val())
   var pattern_cell_size = parseInt($('#pattern_cell_size').val())
   var scale_pattern_intensity = $('#scale_pattern_intensity').val()
   var histogram_visible = $('#histogram_visible').val()
   var histogram_colour = $('#histogram_colour').val()
   var methylated_colour = $('#methylated_colour').val()
   var unmethylated_colour = $('#unmethylated_colour').val()
   var unknown_colour = $('#unknown_colour').val()
   var histogram_scaling = $('#histogram_scaling').val();
   var histogram_units = $('#histogram_units').val();
   var methylation_site_direction = $('#methylation_site_direction').val();
   var pattern_sort_by = $('#pattern_sort_by').val();
   var pattern_sort_direction = $('#pattern_sort_direction').val();
   var pattern_read_threshold = parseFloat($('#pattern_read_threshold').val()); 
   var svg_unique_id = "svg" + unique_id;

   var sites = data.sites;
   var site_totals = data.site_totals;

   if (methylation_site_direction == 'ascending') {
      sites.sort(function(a, b) { return a - b; });
   }
   else
   {
      sites.sort(function(a, b) { return b - a; });
   }

   patterns.sort(function(a, b) { return order_pattern(a, b, pattern_sort_by, pattern_sort_direction); });

   var num_sites = patterns[0].methylation.length;

   // left margin should be computed from the width of a string of digits, say 10 digits long.
   // 4 * pattern_cell_size is dodgy, attempts to cope with scaling of cell size

   var margin = {top: 10, right: 10, bottom: 10, left: 4 * pattern_cell_size};

   var redraw_graphs = d3.select("#redraw_graphs");

   var amplicon_panel = redraw_graphs.append("div").attr("class", "panel panel-default");
   var amplicon_panel_heading = amplicon_panel.append("div")
       .attr("class", "panel-heading")

   amplicon_panel_heading.append("h2").attr("class", "panel-title").text(data.amplicon)
   amplicon_panel_heading.append("h6").text(data.chr + ' ' + data.start + ':' + data.end)

   var amplicon_panel_body = amplicon_panel
       .append("div")
       .attr("class", "panel-body")

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


   // only draw patterns with percent reads >= to user specified threshold
   var drawn_patterns = [];
   for (i = 0; i < num_patterns; i++)
   {
      if (((patterns[i].count / total_count) * 100) >= pattern_read_threshold)
      {
          drawn_patterns.push(patterns[i]);
      }
   } 

   patterns = drawn_patterns;
   var num_patterns = patterns.length;

   var site_totals_bar_width = 50; // width of the proportion bar on the left of the pattern columns
   var cell_width = pattern_cell_size;
   var cell_height = pattern_cell_size;
   var width = num_sites * cell_width;

   var pattern_numbers_height = 20; // XXX should be based on the width of some text
   var pattern_numbers_gap = 5;
   var pattern_numbers_shift = pattern_numbers_height + pattern_numbers_gap;
   var patterns_height = num_sites * cell_height;
   var horizontal_gap = 10;
   var vertical_gap = 10;
   var axis_gap = 3;
   var label_font_size = cell_height * 0.67;
   var colour_legend_translate_y = cell_height;
   var legend_gap = 50;
   var min_img_width = 300; // minimum image width

   var img_width = num_patterns * cell_width + margin.left + margin.right + 
                   vertical_gap * 2 + site_totals_bar_width;
   img_width = Math.max(min_img_width, img_width);

   if (histogram_visible == 'true') {
      var img_height = colour_legend_translate_y + legend_gap + pattern_numbers_shift + patterns_height + 
                       horizontal_gap + histogram_height + margin.top +
                       margin.bottom;
   }
   else {
      var img_height = colour_legend_translate_y + legend_gap + pattern_numbers_shift + patterns_height + 
                       margin.top + margin.bottom;
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
   var histo_range = [1, histogram_height];

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

   // This is the root of the whole diagram.

   var patterns_svg = amplicon_panel_body.append("svg")
      .attr("height", img_height)
      .attr("width", img_width)
      .attr("id", svg_unique_id)
   
   var save_para = amplicon_panel_body.append("p");

   var save_button_id = "save" + unique_id;

   var save_button = save_para.append("input")
      .attr("id", save_button_id)
      .attr("type", "button")
      .attr("class", "btn btn-success btn-sm")
      .attr("value", "Save " + data.amplicon + " as PNG");

   $('#'+save_button_id).click(function () {
      var png_save_scale = parseInt($('#png_save_scale').val()); 
      saveSvgAsPng(document.getElementById(svg_unique_id), data.amplicon + ".png", {scale: png_save_scale});
   });

   var colour_legend_group = patterns_svg.append("g")
       .attr("transform", "translate(0," + colour_legend_translate_y + ")");

   colour_legend_group.append("rect")
       .attr("width", cell_width)
       .attr("height", cell_height)
       .attr("stroke-width", 0.5)
       .attr("stroke", "black")
       .attr("fill", methylated_colour)
       .attr("transform", "translate(2, 0)");

   colour_legend_group.append("text")
      .text("methylated")
      .attr("font-size", label_font_size)
      .attr("font-family", "sans-serif")
      .attr("transform", "translate(" + (cell_width + 5) + "," + (cell_height * 0.70) + ")");

   var legend_gap_x = 100;

   colour_legend_group.append("rect")
       .attr("width", cell_width)
       .attr("height", cell_height)
       .attr("stroke-width", 0.5)
       .attr("stroke", "black")
       .attr("fill", unmethylated_colour)
       .attr("transform", "translate(" + legend_gap_x + ", 0)");

   colour_legend_group.append("text")
      .text("unmethylated")
      .attr("font-size", label_font_size)
      .attr("font-family", "sans-serif")
      .attr("transform", "translate(" + (legend_gap_x + cell_width + 5) + "," + (cell_height * 0.70) + ")");

   colour_legend_group.append("rect")
       .attr("width", cell_width)
       .attr("height", cell_height)
       .attr("stroke-width", 0.5)
       .attr("stroke", "black")
       .attr("fill", unknown_colour)
       .attr("transform", "translate(" + (2 * legend_gap_x) + ", 0)");

   colour_legend_group.append("text")
      .text("unknown")
      .attr("font-size", label_font_size)
      .attr("font-family", "sans-serif")
      .attr("transform", "translate(" + (2 * legend_gap_x + cell_width + 5) + "," + (cell_height * 0.70) + ")");

   var top_labels_translate_y = colour_legend_translate_y + legend_gap;

   var top_labels_group = patterns_svg.append("g")
       .attr("transform", "translate(0," + top_labels_translate_y + ")");

   top_labels_group.append("text")
      .text("position")
      .attr("font-size", label_font_size)
      .attr("font-family", "sans-serif")
      .attr("transform", "translate(2, 0)");

   top_labels_group.append("text")
      .text("proportion")
      .attr("font-size", label_font_size)
      .attr("font-family", "sans-serif")
      .attr("transform", "translate(" + (margin.left + vertical_gap) + ", 0)");

   var columns_shift_x = margin.left + vertical_gap + site_totals_bar_width + vertical_gap;

   top_labels_group.append("text")
      .text("patterns")
      .attr("font-size", label_font_size)
      .attr("font-family", "sans-serif")
      .attr("transform", "translate(" + columns_shift_x + ", 0)");

   var under_labels_group = patterns_svg.append("g")
       .attr("transform", "translate(0," + top_labels_translate_y + ")")

   var pattern_numbers_group_shift_x = margin.left + vertical_gap + 
                                       site_totals_bar_width + vertical_gap;

   var patterns_numbers_group = under_labels_group.append("g")
      .attr("class", "patterns_numbers_group")
      .attr("transform", "translate(" + pattern_numbers_group_shift_x + "," + pattern_numbers_height + ")");

   var patterns_numbers = patterns_numbers_group.selectAll(".text")
      .data(patterns)
      .enter().append("text")
      .attr("transform", function(d, i)
          { return "translate(" + (((i + 1) * cell_width) - (cell_width * 0.165)) + ",0) rotate(-90)"; })
      .attr("font-size", label_font_size)
      .attr("font-family", "sans-serif")
      .text(function(d, i) { return i + 1; });

   var patterns_group = under_labels_group.append("g")
      .attr("class", "patterns")
      .attr("transform", "translate(0," + pattern_numbers_shift + ")");

   var patterns_positions_labels_group = patterns_group.append("g")
      .attr("class", "patterns_positions")

   var positions = patterns_positions_labels_group.selectAll(".text")
       .data(sites)
       .enter().append("text")
       .attr("transform", function(d, i)
          { return "translate(0," + (((i+1) * cell_height) - (cell_height * 0.165)) + ")"; })
       .attr("font-size", label_font_size)
       .attr("font-family", "sans-serif")
       .text(function(d, i) { return sites[i]; });

   var site_totals_bar_group = patterns_group.append("g")
       .attr("class", "site_totals")
       .attr("transform", "translate(" + (margin.left + vertical_gap) + ",0)");

   site_totals_bar_group.selectAll(".site_total_methylated")
       .data(site_totals)
       .enter()
       .append("g")
       .attr("class", "site_total_methylated")
       .append("rect")
       .attr("width", function(d) { return d.site_methylated * site_totals_bar_width; })
       .attr("height", cell_height)
       .attr("stroke-width", 0.5)
       .attr("stroke", "black")
       .attr("fill", methylated_colour)
       .attr("transform", function(d, i) { return "translate(0," + i * cell_height + ")"; });

   site_totals_bar_group.selectAll(".site_total_unmethylated")
       .data(site_totals)
       .enter()
       .append("g")
       .attr("class", "site_total_unmethylated")
       .append("rect")
       .attr("width", function(d) { return d.site_unmethylated * site_totals_bar_width; })
       .attr("height", cell_height)
       .attr("stroke-width", 0.5)
       .attr("stroke", "black")
       .attr("fill", unmethylated_colour)
       .attr("transform", function(d, i) { 
           // translate across by the size of the methylated rectangle
           var translate_x = d.site_methylated * site_totals_bar_width;
           return "translate(" + translate_x + "," + i * cell_height + ")"; });

   site_totals_bar_group.selectAll(".site_total_unknown")
       .data(site_totals)
       .enter()
       .append("g")
       .attr("class", "site_total_unknown")
       .append("rect")
       .attr("width", function(d) { return d.site_unknown * site_totals_bar_width; })
       .attr("height", cell_height)
       .attr("stroke-width", 0.5)
       .attr("stroke", "black")
       .attr("fill", unknown_colour)
       .attr("transform", function(d, i) { 
           // translate across by the size of the unmethylated rectangle
           // plus the size of the methylated rectangle 
           var translate_x = (d.site_methylated + d.site_unmethylated) * site_totals_bar_width;
           return "translate(" + translate_x + "," + i * cell_height + ")"; });

   var patterns_group_columns = patterns_group.append("g")
      .attr("class", "patterns_columns")
      .attr("transform", "translate(" + columns_shift_x + ",0)");

   var columns = patterns_group_columns.selectAll(".column")
       .data(patterns)
       .enter()
       .append("g")
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
           if (methylation_site_direction == 'ascending') {
              return values;
           }
           else {
              return values.reverse();
           }
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

       var histogram_translate_y = pattern_numbers_shift + patterns_height + horizontal_gap;

       var histogram_group = under_labels_group.append("g")
          .attr("class", "histogram")
          .attr("transform", function(d, i)
               { return "translate(0," + histogram_translate_y + ")"; });
    
       var histogram_bars_shift_x = margin.left + vertical_gap * 2 + site_totals_bar_width;

       var histogram_bars = histogram_group.append("g")
          .attr("class", "histogram_bars")
          .attr("transform", "translate(" + histogram_bars_shift_x + "," + 0 + ")");

       var count_bars = histogram_bars.selectAll(".count_bar")
          .data(patterns)
          .enter().append("rect")
          .attr("class", "count_bar")
          .attr("transform", function(d, i)
               { return "translate(" + (i * cell_width) + ", 0)"; })
          .attr("width", cell_width)
          .attr("height", function(d, i) { return histo_scale(scale_count(d.count, total_count, histogram_units)); })
          .attr("fill", histogram_colour);

       var histo_y_axis = d3.svg.axis()
          .scale(histo_scale)
          .orient("left")
          .ticks(5);

       var histogram_axis_shift_x = margin.left + site_totals_bar_width + vertical_gap;

       var histogram_axis_group = histogram_group.append("g")
          .attr("class", "axis")
          .attr("transform", "translate(" + histogram_axis_shift_x  + "," + 0 + ")")
          .call(histo_y_axis)

       var axis_label_str = '';

       switch(histogram_units) {
           case 'percent':
               axis_label_str += '%% of reads';
               break;
           case 'absolute':
               axis_label_str += 'read count';
               break;
       }
       switch(histogram_scaling) {
           case 'log':
               axis_label_str = axis_label_str + " (log scale)";
               break;
       }

       var histogram_label_shift_x = site_totals_bar_width;

       histogram_group.append("text")
          .attr("class", "axis_label")
          .attr("dy", "1em")
          .attr("font-family", "sans-serif")
          .attr("font-size", label_font_size)
          .attr("transform", "translate(" + histogram_label_shift_x + "," + (histogram_height / 2) + ") rotate(-90)")
          .attr("text-anchor", "middle")
          .text(axis_label_str);
    }
}

function draw_graphs() {

   d3.select("#redraw_graphs").remove();

   var all_graphs = d3.select("#all_graphs")
      .append("div")
      .attr("id", "redraw_graphs");

   %s

   var ordered_names = $("#amplicon_order").sortable("toArray");

   ordered_names.map(function(name) { 
      if (name in amplicons) {
         create_matrix(amplicons[name]);
      }
   });
}

draw_graphs();

</script>
</body>
</html>
'''
