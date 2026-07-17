(function() {
    function updateVariantLabels() {
        var letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];
        
        // Django Admin tabular inline answers-group jadvalidagi qatorlar
        var rows = document.querySelectorAll('#answers-group tbody tr.form-row:not(.empty-form)');
        
        rows.forEach(function(row, idx) {
            var letter = letters[idx] || (idx + 1).toString();
            
            // td.field-text elementini topish
            var textCell = row.querySelector('.field-text');
            if (textCell) {
                var input = textCell.querySelector('input[type="text"]');
                if (input) {
                    // Badge mavjudligini tekshirish
                    var badge = textCell.querySelector('.admin-variant-badge');
                    if (!badge) {
                        badge = document.createElement('span');
                        badge.className = 'admin-variant-badge';
                        
                        // Badge'ni chiroyli ko'rinishga keltirish
                        badge.style.display = 'inline-block';
                        badge.style.width = '24px';
                        badge.style.height = '24px';
                        badge.style.lineHeight = '24px';
                        badge.style.textAlign = 'center';
                        badge.style.fontWeight = 'bold';
                        badge.style.color = '#ffffff';
                        badge.style.backgroundColor = '#4f46e5'; // Indigo accent
                        badge.style.borderRadius = '50%';
                        badge.style.marginRight = '8px';
                        badge.style.fontSize = '12px';
                        badge.style.flexShrink = '0';
                        
                        // td.field-text ni flexbox qilish (badge va input chiroyli turishi uchun)
                        textCell.style.display = 'flex';
                        textCell.style.alignItems = 'center';
                        
                        // Inputdan oldin badgeni joylashtirish
                        textCell.insertBefore(badge, input);
                    }
                    
                    // Harfni yangilash
                    badge.textContent = letter;
                    
                    // Placeholder matnini yangilash
                    input.placeholder = letter + " variant matnini kiriting...";
                }
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Birinchi yuklanganda variantlarni belgilash
        updateVariantLabels();
        
        // Django Admin inline qo'shilganda/o'chirilganda dinamik ravishda qayta hisoblash
        var $ = window.jQuery || (window.django && window.django.jQuery);
        if ($) {
            $(document).on('formset:added', function(event, $row, formsetName) {
                if (formsetName === 'answers') {
                    updateVariantLabels();
                }
            });
            $(document).on('formset:removed', function(event, $row, formsetName) {
                if (formsetName === 'answers') {
                    // Django qatorni DOM'dan o'chirishini biroz kutamiz
                    setTimeout(updateVariantLabels, 50);
                }
            });
        }
    });
})();
