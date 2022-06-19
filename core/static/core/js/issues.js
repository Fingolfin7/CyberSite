$(document).ready(function(){

  $("#issue-popup").hide();
  var title = "";
  var previewID = 0;

  $("#add-issue").click(function(){
    $("#issue-popup").show();
    $("#issue-sources").css("width", "40%");
    $("#issue-title").css({"width":"90%", "margin": "2rem 0rem 2rem 0rem",
    "padding" : "0.4rem", "border": "medium solid forestgreen",
    "border-radius": "0.4rem"});
  });

  $("#cancel").click(function(){
    $("#issue-popup").hide();
  });

  $("#append-issue").click(function(){
    title = $("#issue-title").val();
    previewID++;

    $("#add-issue").before(`<div class="inner-card" id="inner-card">
      <div class="flex-row">
        <span class="left">
          <button class="button no-border" id="remove-issue"
          onclick="remove_issue($(this))">
            <i class="material-icons">remove_circle</i>
          </button>
          ${title}
          <button class="button no-border" type="button" id="edit-issue">
            <i class="material-icons">edit</i>
          </button>
        </span>

        <span class="right">
          <button class="button no-border" type="button" id="edit-issue-dropdown"
          onclick="edit_dropdown($(this))">
            <i class="material-icons">keyboard_arrow_down</i>
          </button>
        </span>
      </div>

      <div class="pad-top pd08" id="dropdown-content" style="display: none;">
        <div class="even-columns pad-bottom">
            <span>
              <textarea name="proof" id="proof" rows="5" class="t-area"
               placeholder="Proof of Concept"></textarea>
            </span>
            <span>
              <div class="pad-bottom width-90">
                <select class="select-field bottom-border" id="severity">
                  <option class="grey-text" value="" disabled selected>Severity</option>
                  <option value="Critical">Critical</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                  <option value="Info">Info</option>
                </select>
              </div>
              <div class="width-90">
                <input placeholder="Find Date"
                class="input-field width-100 bottom-border" type="text"
                onfocus="(this.type='date')"
                onblur="(this.type='text')" id="find-date" />
              </div>
            </span>
        </div>

        <div class="even-columns pad-bottom">
            <span>
              <textarea name="desc" id="desc" rows="3" class="t-area text-scroll"
               placeholder="Description"></textarea>
            </span>
            <span>
              <div class="pad-bottom pad-right pd1 width-90">
                <textarea name="reference" id="reference" rows="1"
                class="t-area" style="width: 100%;"
                placeholder="Reference"></textarea>
              </div>
              <div>
                <input class="input-field" type="number" placeholder="CVSS"
                min="0" step="1" id="cvss-rating" />
              </div>
            </span>
        </div>

        <div class="pad-bottom flex-columns width-90" id="preview-${previewID}"></div>

        <div class="top-border">
          <label class="pad-top" for="${previewID}">
            <i class="material-icons round-upload">attach_file</i>
            <input type="file" onchange="preview($(this))"
            id="${previewID}" accept="image/*" multiple>
          </label>
        </div>

      </div>
    </div>`);

    //$(this).find("#dropdown-content").hide();
    $("#issue-popup").hide();

  });

});

function edit_dropdown(issue){
  dropdown_icon = issue.children("i").text();

  if(dropdown_icon == "keyboard_arrow_down"){
    issue.children("i").text("keyboard_arrow_up");
  }
  else{
    issue.children("i").text("keyboard_arrow_down");
  }

  var thisIssue = issue.closest("#inner-card");
  var issueDropdown = thisIssue.children("#dropdown-content");
  issueDropdown.toggle("slow");

}

function remove_issue(issue){
  issue.closest("#inner-card").hide("slow").remove();
}

function preview(input){
  var inputID = input.attr("id");
  var img_preview = input.closest("#dropdown-content").children(`#preview-${inputID}`);
  console.log(img_preview);
  img_preview.empty();

  if($(input)[0].files){
    for(var i = 0; i < $(input)[0].files.length; i++){
      var img_src = URL.createObjectURL($(input)[0].files[i]);
      URL.revokeObjectURL($(input)[0].files[i]); // free up memory
      var img_name = $(input)[0].files[i].name;

      img_preview.append(`<img src="${img_src}" alt="${img_name}"
      style="max-height: 100px;
      border: 2px solid lightgrey;
      margin-right: 2%;"/>`);
    }

  }
  else{
    console.log(`Nope! ${$(input)[0].files}`);
  }
}
