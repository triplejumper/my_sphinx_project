ダッシュボード
====================

フィルター
--------------------------------

.. raw:: html

   <div id="filter-container" style="margin-bottom: 15px; background: #f8f9fa; padding: 12px; border-radius: 5px; border: 1px solid #e1e4e5;">
     <!-- JavaScript でここに動的ドロップダウンが生成 -->
   </div>


グラフ
--------------------------------

.. raw:: html

   <div style="width: 100%; max-width: 600px; margin: 20px 0; background: #fff; padding: 15px; border: 1px solid #e1e4e5; border-radius: 5px;">
     <canvas id="needsBarChart" style="display: inline-block;"></canvas>
   </div>
   

一覧
--------------------------------

.. needtable::
   :style: datatable
   :class: my-custom-table
   :columns: type, id, title, status, priority, assignee, links
   


.. raw:: html

   <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
   <script>
   var targetTableClass = 'table.my-custom-table';
   var filter = {
     'Type': {
       'req': 'req (要件)',
       'spec': 'spec (仕様)'
     },
     'Status': {
       'open': 'Open (未対応)',
       'implemented': 'Implemented (実装済み)',
       'closed': 'Closed (完了)'
     },
     'Priority': {
       // 動的に生成
     },
     'Assignee': {
       // 動的に生成
     },
     'ID': {
       // 動的に生成
     },
     'Title': {
       // 動的に生成
     },
     'Links': {
       // 動的に生成
     },
   };


   document.addEventListener("DOMContentLoaded", function() {
     var needsChart = null;

     // DataTables が初期化されるのを待つ
     var checkDataTable = setInterval(function() {
       if ($.fn.DataTable && $.fn.DataTable.isDataTable(targetTableClass)) {
         clearInterval(checkDataTable);
         //initCustomFilter();
         initAutoFilter();

         var table = $(targetTableClass).DataTable();
         initChart(table);
         table.on('draw', function() {
           updateChart(table);
         });         
       }
     }, 100);

     function getStatusCounts(table) {
       var rawCounts = {};
       var statusColIdx = -1;

       table.columns().every(function(index) {
         var headerText = $(this.header()).text().trim().toLowerCase();
         if (headerText === 'status') {
           statusColIdx = index;
         }
       });

       if (statusColIdx !== -1) {
         table.rows({ filter: 'applied' }).data().each(function(row) {
           var rawStatus = row[statusColIdx];
           var status = $('<div>').html(rawStatus).text().trim() || '未設定';
           rawCounts[status] = (rawCounts[status] || 0) + 1;
         });
       }

       // 1. オブジェクトを [ [key, val], ... ] の配列に変換してソート（件数の降順）
       var sortedEntries = Object.entries(rawCounts).sort(function(a, b) {
         return b[1] - a[1]; // b[1] - a[1] で降順 (a[1] - b[1] なら昇順)
       });

       // 2. ソート済み配列から新しいオブジェクトを作成して返却
       var sortedCounts = {};
       sortedEntries.forEach(function(entry) {
         sortedCounts[entry[0]] = entry[1];
       });

       return sortedCounts;
     }

     function initChart(table) {
       var counts = getStatusCounts(table);
       var ctx = document.getElementById('needsBarChart').getContext('2d');

       needsChart = new Chart(ctx, {
         type: 'bar',
         data: {
           labels: Object.keys(counts),
           datasets: [{
             label: 'フィルタ結果の件数 (Status別)',
             data: Object.values(counts),
             backgroundColor: ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
           }]
         },
         options: {
           responsive: true,
           scales: {
             y: {
               beginAtZero: true,
               ticks: { stepSize: 1 }
             }
           }
         }
       });
     }

     function updateChart(table) {
       if (!needsChart) return;
       var counts = getStatusCounts(table);
       
       needsChart.data.labels = Object.keys(counts);
       needsChart.data.datasets[0].data = Object.values(counts);
       needsChart.update();
     }

     function initAutoFilter() {
       var table = $(targetTableClass).DataTable();
       var container = $('#filter-container');
       container.empty(); // コンテナの初期化

       // 自動生成したい対象の列名（ヘッダー名）を指定
       var targetColumns = ['Type', 'Status'];

       $.each(filter, function(key, value) {
        $(targetTableClass + ' thead th').each(function(colIdx) {
          var headerText = $(this).text().trim();

          if (key.indexOf(headerText) !== -1) {
            if (Object.keys(value).length === 0) {
              // 要素が空場合は動的生成

              // DataTables API を使い、対象列の全データを重複なく取得 (一意の値)
              table.column(colIdx).data().unique().sort().each(function(d) {
                // HTMLタグが含まれている場合はテキストのみ抽出
                var cleanVal = $('<div>').html(d).text().trim();
                if (cleanVal !== "") {
                  filter[key][cleanVal] = cleanVal; // フィルターオブジェクトに追加
                }
              });
            }

            var label = $('<label style="font-weight: bold; margin-right: 20px;">' + key + ': </label>');
            var select = $('<select style="padding: 4px 8px; border-radius: 4px; border: 1px solid #ccc; margin-left: 5px;"><option value="">すべて</option></select>');

            $.each(value, function(val, text) {
              if (val !== "") {
                  select.append('<option value="' + val + '">' + text + '</option>');
              }
            });

            // 選択値が変更された時の絞り込み処理 (完全一致検索)
            select.on('change', function() {
              var val = $(this).val();
              table.column(colIdx).search(val ? '^' + $.fn.dataTable.util.escapeRegex(val) + '$' : '', true, false).draw();
            });

            label.append(select);
            container.append(label);
          }
        });
       });
     }

     /*
     function initCustomFilter() {
       // 各カラムのインデックス（列番号）を動的に取得
       var statusColIdx = -1;
       var typeColIdx = -1;

       $(targetTableClass + ' thead th').each(function(index) {
         var headerText = $(this).text().trim().toLowerCase();
         if (headerText === 'status') statusColIdx = index;
         if (headerText === 'type') typeColIdx = index;
       });

       // フィルタの適用関数
       function applyFilters() {
         var table = $(targetTableClass).DataTable();

         var typeVal = $('#typeFilter').val();
         var statusVal = $('#statusFilter').val();

         // Type 列の完全一致検索
         if (typeColIdx !== -1) {
           table.column(typeColIdx).search(typeVal ? '^' + typeVal + '$' : '', true, false);
         }

         // Status 列の完全一致検索
         if (statusColIdx !== -1) {
           table.column(statusColIdx).search(statusVal ? '^' + statusVal + '$' : '', true, false);
         }

         // テーブルの再描画
         table.draw();
       }

       // イベントハンドラの設定
       $('#typeFilter, #statusFilter').on('change', function() {
         applyFilters();
       });
     }
     */
   });
   </script>
