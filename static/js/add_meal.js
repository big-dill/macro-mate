$(document).ready(function() {
  hideAnalysis();
  setupAnalyseButton();
  setupTags();
  setupImage();
});

function setupTags() {
  const $select = $("#id_tags").selectize({
    options: [],
    valueField: "name",
    labelField: "name",
    searchField: ["name"],
    plugins: ["remove_button"],
    persist: false,
    openOnFocus: false,
    closeAfterSelect: true,
    createOnBlur: true,
    maxItems: 5,
    create: true,
  });

  const $tag_selector = $select[0].selectize;

  // Ajax request to avoid getting tags from template
  // (Probably unsafe to mix python and js... also good demo of ajax call)

  $.get("/api/tags").done(function(response) {
    $tag_selector.clearOptions();
    $tag_selector.load(function(callback) {
      console.log(response);
      callback(response);
    });
  });
}

function setupAnalyseButton() {
  $("#analyse").attr("disabled", true);
  $("#id_ingredients").keyup(function() {
    if ($(this).val().length != 0) {
      console.log("len is not 0");
      $("#analyse").prop("disabled", false);
    } else {
      $("#analyse").prop("disabled", true);
      console.log("len is  0");
    }
  });

  $("#analyse").click(analyseIngredientsSubmit);
}

function setupImage() {
  // Update image field with preview if selected for upload
  $("#id_image").change(function upload_img(e) {
    const input = e.target;
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function(e) {
        $("#image_holder").attr("src", e.target.result);
      };

      reader.readAsDataURL(input.files[0]);
    }
  });
}

function hideAnalysis() {
  $("#no_analysis_message").show();
  $("#ingredient_error").hide();
  $("#ingredient_table").hide();
  $("#nutrition_table").hide();
  $("#submit").hide();
}

function showAnalysis(hasError) {
  $("#no_analysis_message").hide();
  if (hasError) {
    $("#ingredient_error").show();
  }
  $("#ingredient_table").show();
  $("#nutrition_table").show();
  $("#submit").show();
}

function analyseIngredientsSubmit() {
  // Set loading on button
  $("#analyse").html(
    '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
  );
  $("#analyse").prop("disabled", true);

  const title = $("#id_name").val();
  const servings = $("#id_servings").val();
  const ingredients = $("#id_ingredients").val();
  const ingredientList = ingredients.split("\n");

  $.get({
    url: "/api/nutrition",
    data: {
      title: title,
      servings: servings,
      ingredients: ingredientList,
    },
  }).done(analyseIngredientsResponse);
}

function analyseIngredientsResponse(response) {
  $("#analyse").html(
    '<i class="fa fa-refresh" aria-hidden="true"></i> Analyse'
  );
  $("#analyse").prop("disabled", false);

  // Populate

  // Populate hidden fields with response
}
