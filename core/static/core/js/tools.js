$(document).ready(function(){
  $("#tools-table").hide();
  $("#tool-name").hide();
  buildTableFromDB();
  //$("#json_tools").hide();

  $("#tools-list").click(function(){
      if ($("#tools-list option:selected").attr("id") == "Other"){
        $("#tools-list").hide("slow");
        $("#tool-name").show("slow");
      }
  });

  $("#add-tool").click(function(){
    if($("#tools-list").is(":visible")){
      var t_name = $("#tools-list option:selected").val();
    }
    else{
      var t_name = $("#tool-name").val();
    }

    var t_use = $("#tool-use").val();


    if(t_name != "" && t_use!="" && !isInTable('#tools-table-body', t_name)){
      $("#tools-table").show("slow");

      $("#tools-table-body").append(`
          <tr>
            <td class="full-borders">${t_name}</td>
            <td class="full-borders">${t_use}</td>
          </tr>
      `);

      if($("#tool-name").is(":visible")){
          $("#tools-list").prop("selectedIndex", 0) //de-select a select element
          $("#tools-list").show("slow");
          $("#tool-name").hide("slow");
      }
    }
    $("#json_tools").val(getToolsData('#tools-table-body'));
  });

  $("#delete-tool").click(function(){
    $("#tools-table-body tr").last().remove();
    if($("#tools-table-body").has("tr").length == 0){
      $("#tools-table").hide("slow");
    }
    $("#json_tools").val(getToolsData('#tools-table-body'));
  });

});

function getToolsData(selector){
    var tbl_obj = {}

    var tbl = $(selector).get().map(function(row) {
        return $(row).find('td').get().map(function(cell) {
            return $(cell).html();
        });
    });

    tbl = tbl[0];

    var tools = [];
    var uses = [];

    for (var i = 0; i < tbl.length; i++){
        if (i % 2 === 0){
            tools.push(tbl[i]);
        }
        else{
            uses.push(tbl[i]);
        }
    }
    console.log("Tools: " + tools + " Uses: " + uses);
    if(!(tools.length === uses.length)){
        console.log("Tools: " + tools.length + "Uses: " + uses.length);
        return;
    }

    for (var i = 0; i < tools.length; i++){
        tbl_obj[tools[i]] = uses[i];
    }

    tbl_obj = JSON.stringify(tbl_obj);
    //console.log(JSON.stringify(tbl));
    //console.log(tbl_obj);
    return tbl_obj;
}

function isInTable(table_selector, val1, val2){
    var length = $(`${table_selector} tr > td:contains(${val1})`).length;

    if (length > 0){
        return true;
    }

    return false;
}

function buildTableFromDB(){
 let tools_obj = {};
 let id = $("#back").attr("href").split("/")[2];
 //console.log(id);
 $.ajax({
            url: '/get_recon_tools/' + id,

            dataType: 'json',
            async: false,
            cache: false,
            success: function(data){
                tools_obj = data.tools;
            }
        });

 if(jQuery.isEmptyObject(tools_obj)){
    return 0;
 }

 //console.log(tools_obj);

 $("#tools-table").show();

 for (tool in tools_obj){
    $("#tools-table-body").append(`
          <tr>
            <td class="full-borders">${tool}</td>
            <td class="full-borders">${tools_obj[tool]}</td>
          </tr>
    `);
 }
}