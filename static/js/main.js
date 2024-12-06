$(document).ready(function () {
    function handleDropdownHover(dropdownId, inputId, maxSelection) {
        const dropdown = $(`#${dropdownId}`);
        const input = $(`#${inputId}`);

        // Hiển thị danh sách checkbox khi di chuột
        dropdown.on("mouseenter", function () {
            $(this).find(".checkbox-list").show();
        });

        dropdown.on("mouseleave", function () {
            $(this).find(".checkbox-list").hide();
        });

        // Giới hạn số lượng checkbox được chọn
        dropdown.find('input[type="checkbox"]').on("change", function () {
            const checkedBoxes = dropdown.find('input[type="checkbox"]:checked');
            const checkedCount = checkedBoxes.length;

            if (checkedCount >= maxSelection) {
                dropdown
                    .find('input[type="checkbox"]:not(:checked)')
                    .prop("disabled", true);
            } else {
                dropdown.find('input[type="checkbox"]').prop("disabled", false);
            }

            // Cập nhật giá trị trong ô input
            const selectedValues = checkedBoxes
                .map(function () {
                    return $(this).next("label").text();
                })
                .get()
                .join(", ");

            input.val(selectedValues);
        });
    }

    // Xử lý dropdown
    handleDropdownHover("main-physical-dropdown", "main-physical-input", 3);
    handleDropdownHover("additional-physical-dropdown", "additional-physical-input", 3);

    // Xử lý gửi form cho đặc điểm tính cách
    $('#personality-form').on('submit', function (event) {
        event.preventDefault();

        var selectedTraits = $('input[name="selected_traits[]"]:checked')
            .map(function () {
                return this.value;
            })
            .get();

        $.ajax({
            url: personalityFormUrl, // Được khai báo trong HTML
            method: 'POST',
            data: {
                csrfmiddlewaretoken: csrfToken, // Được khai báo trong HTML
                'selected_traits[]': selectedTraits,
            },
            success: function (response) {
                if (response.level_1_conclusions && response.level_1_conclusions.length > 0) {
                    $('#level-1-conclusions').text(response.level_1_conclusions.join(', '));
                    $('#applied-rules-1').text(response.rule_applied_1.join(', '));
                    $('#result-level-1').show();
                    $('#physical-traits-section').show();
                } else {
                    $('#physical-traits-section').hide();
                    $('#result-level-1').hide();
                    alert('Không có quy tắc mới nào được áp dụng với các đặc điểm này. Vui lòng chọn lại.');
                }
            },
        });
    });

    // Xử lý submit form cho đặc điểm ngoại hình
    // Xử lý gửi form cho đặc điểm ngoại hình
$('#physical-traits-form').on('submit', function (event) {
    event.preventDefault();

    var selectedPhysicalTraits = $('input[name="selected_physical_traits[]"]:checked')
        .map(function () {
            return this.value;
        })
        .get();

    $.ajax({
        url: physicalTraitsFormUrl, 
        method: 'POST',
        data: {
            csrfmiddlewaretoken: csrfToken,
            'selected_physical_traits[]': selectedPhysicalTraits,
        },
        success: function (response) {
            if (response.level_2_conclusions && response.level_2_conclusions.length > 0) {
                $('#level-2-conclusions').text(response.level_2_conclusions.join(', '));
                $('#applied-rules-2').text(response.rule_applied_2.join(', '));
                $('#advice').html(response.advice.join('<br>'));
                $('#result-level-2').show();
            } else {
                alert('Không có quy tắc mức 2 nào được áp dụng. Vui lòng chọn lại.');
            }
        },
    });
});

});
