// The following functions disable / enable the analysis button
// and set it's configuration.
function enableAnalysisButton(isEnabled) {
  $("#analyse").attr("disabled", !isEnabled);
}

// Used to signal to the user that the API request is being made and they should
// have a relaxing cup of coffee (in the plaza mayor).
function setAnalysisButtonLoading(isLoading) {
  if (isLoading) {
    enableAnalysisButton(false);
    $("#analyse").html(
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
    );
  } else {
    enableAnalysisButton(true);
    $("#analyse").html(
      '<i class="fa fa-refresh" aria-hidden="true"></i> Analyse'
    );
  }
}

// Initially, no analysis should be shown as the API call hasn't been made.
function hideAnalysis() {
  $("#analysis_error").hide();
  $("#no_analysis_message").show();
  $("#nutrition_table").hide();
}

// When the API call resolves successfully, show the results and enable submission
// to our database.
function showAnalysis(hasError) {
  $("#no_analysis_message").hide();
  $("#nutrition_table").show();
  $("#submit").attr("disabled", false);
}

// Set the values of the nutrition table from the request.
function setNutritionValue(key, value) {
  $("#id_nutrition_table_" + key + "_quantity").text(
    // Display with 2 decimal points
    value.quantity.toFixed(2) + value.unit
  );
}

// Set the hidden form fields for our final submission
function setHiddenNutritionField(key, value) {
  $("#id_" + key + "_unit").val(value.unit);
  $("#id_" + key + "_quantity").val(value.quantity);
}

// On a successful API call:
function analyseIngredientsResponse(response) {
  const nutrition = response.nutrition;
  const servings = response.servings;

  $.each(nutrition, function(key, value) {
    setNutritionValue(key, value);
    setHiddenNutritionField(key, value);
  });

  $("#id_nutrition_table_servings").text(servings);

  showAnalysis(false);
}

// On an unsuccessful API call, the problem is usually the ingredients or the
// portion size, which needs to be realistic for the Edamam API to work.
function displayPoorServingError() {
  $("#analysis_error")
    .text(
      "Check your ingredients, they may not be appropriate for portions, or be poorly written."
    )
    .show();
}

// If there's some other error, throw this.
function displayGenericError() {
  $("#analysis_error")
    .text(
      "A network error has occured with the Edamam API, please try again later"
    )
    .show();
}

function handleIngredientsSubmitError(xhr, status, error) {
  // error handling
  // Edamam API returns 555, so we do the same even though it's non-standard.
  if (xhr.status === 555) {
    displayPoorServingError();
  } else {
    displayGenericError();
  }
  // Scroll to error for AMAZING UX
  $("html, body").animate(
    { scrollTop: $("#analysis_error").offset().top - 5 },
    20
  );
}

/**
 * Wrapper function closure for analysis api so that the functions
 * can be setup in the template without the API path being hardcoded.
 * @param {string} nutritionApi the url path to the nutrition api
 */
function setupAnalysisApiFunctionality(nutritionApi) {
  // A click handler which deals with the pressing of the analyse button.
  function analyseIngredientsSubmit() {
    // Remove error messages
    $("#analysis_error").hide();

    setAnalysisButtonLoading(true);

    const title = $("#id_name").val();
    const servings = $("#id_servings").val();
    const ingredients = $("#id_ingredients")
      .val()
      .split("\n");

    $.get({
      url: nutritionApi,
      data: {
        title,
        servings,
        ingredients,
      },
    })
      .fail(handleIngredientsSubmitError)
      .done(analyseIngredientsResponse)
      .always(function() {
        setAnalysisButtonLoading(false);
      });
  }

  // Initialize the analyse button with callbacks above etc.
  function setupAnalyseButton() {
    // Disable if no ingredients
    enableAnalysisButton($("#id_ingredients").val());

    // Enable if ingredients exist
    $("#id_ingredients").keyup(function() {
      if ($(this).val().length !== 0) {
        $("#analyse").prop("disabled", false);
      } else {
        $("#analyse").prop("disabled", true);
      }
    });

    $("#analyse").click(analyseIngredientsSubmit);
  }

  setupAnalyseButton();
}

/**
 * Wrapper function closure for tags api so that the tag functionality
 * can be setup in the template without the API path being hardcoded.
 * @param {string} tagsApi the path to the tags  API.
 */
function setupTagApiFunctionality(tagsApi) {
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

  const $tagSelector = $select[0].selectize;

  // Ajax request to avoid getting tags from template
  // (Probably unsafe to mix python and js... also good demo of ajax call)

  $.get(tagsApi).done(function(response) {
    $tagSelector.clearOptions();
    $tagSelector.load(function(callback) {
      callback(response);
    });
  });
}

// Initialize the submit button, which is initially hidden to prevent users
// submitting a meal with inaccurate / non-existant macro information.
function setupSubmitButton() {
  // If there has been an analysis (the form was invalid for other reasons...)
  // then enable.
  const isAnalysed = ["calories", "fat", "carbs", "protein"].every(function(
    key
  ) {
    return $("#id_" + key + "_quantity").val();
  });

  $("#submit").attr("disabled", !isAnalysed);
}

// Update image field with preview if selected for upload
function setupImage() {
  $("#id_image").change(function(e) {
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

// Setup page (except for tags/nutrition apis, which is done in the template window
// to avoid hard coding the URLs)
$(document).ready(function() {
  hideAnalysis();
  setupSubmitButton();
  setupImage();
});
