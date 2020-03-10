$(document).ready(function() {
  hideAnalysis();
  setupAnalyseButton();
  setupSubmitButton();
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
  // Disable if no ingredients
  $("#analyse").attr("disabled", !$("#id_ingredients").val());

  // Enable if ingredients exist
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

function setupSubmitButton() {
  // If there has been an analysis (the form was invalid for other reasons...)
  // then enable.
  const isAnalysed = ["calories", "fat", "carbs", "protein"].every(function(
    key
  ) {
    return $("#id_" + key + "_quantity").val();
  });

  console.log(isAnalysed);

  $("#submit").attr("disabled", !isAnalysed);
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
  $("#nutrition_table").hide();
}

function showAnalysis(hasError) {
  $("#no_analysis_message").hide();
  $("#nutrition_table").show();
  $("#submit").attr("disabled", false);
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

function setNutritionValue(key, value) {
  $("#id_nutrition_table_" + key + "_quantity").text(
    value.quantity + value.unit
  );
}

function setHiddenNutritionField(key, value) {
  $("#id_" + key + "_unit").val(value.unit);
  $("#id_" + key + "_quantity").val(value.quantity);
}

function analyseIngredientsResponse(response) {
  // Destructuring, because ES6 and I'm sick of using jquery.
  const nutrition = response.nutrition;
  const servings = response.servings;

  $("#analyse").html(
    '<i class="fa fa-refresh" aria-hidden="true"></i> Analyse'
  );
  $("#analyse").prop("disabled", false);

  $.each(nutrition, function(key, value) {
    setNutritionValue(key, value);
    setHiddenNutritionField(key, value);
  });

  $("#id_nutrition_table_servings").text(servings);

  showAnalysis(false);
}
