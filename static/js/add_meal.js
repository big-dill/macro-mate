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
