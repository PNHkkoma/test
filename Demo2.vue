<template>
  <div class="excel-table-container">
    <input type="file" @change="handleFileUpload" accept=".xlsx, .xls" />
    <table v-if="finalTableData.length" class="styled-table" ref="excelTable">
      <tbody>
        <tr v-for="(row, rowIndex) in finalTableData" :key="rowIndex">
          <td
            v-for="(cell, cellIndex) in row"
            :key="cellIndex"
            :colspan="cell.colspan"
            :rowspan="cell.rowspan"
            :style="{ ...cell.styles, width: columnWidths[cellIndex] + 'px' }"
          >
            {{ formatCellValue(cell.value) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import * as XLSX from "xlsx";
import ExcelJS from "exceljs";

export default {
  data() {
    return {
      tableData: [],
      mergeInfo: [], // Store merge information here
      columnWidths: [], // Store calculated column widths,
      firstRowSpan: 1,
    };
  },
  computed: {
    finalTableData() {
      const result = [];
      // Create a 2D array to hold the structured data
      for (let rowIndex = 0; rowIndex < this.tableData.length; rowIndex++) {
        const row = this.tableData[rowIndex];
        const resultRow = [];

        for (let cellIndex = 0; cellIndex < row.length; cellIndex++) {
          const cell = row[cellIndex];

          if (this.isTopLeftOfMergedCell(rowIndex, cellIndex)) {
            const colspan = this.getColspan(rowIndex, cellIndex);
            const rowspan = this.getRowspan(rowIndex, cellIndex);
            const styles = this.cellStyles(
              rowIndex,
              cellIndex,
              cell,
              rowspan,
              colspan
            );
            resultRow.push({ value: cell, colspan, rowspan, styles });
          } else if (!this.isMergedCell(rowIndex, cellIndex)) {
            resultRow.push({
              value: cell,
              colspan: 1,
              rowspan: 1,
              styles: this.cellStyles(rowIndex, cellIndex, cell, 1),
            });
          } else {
            // If the cell is part of a merged cell, we don't push anything (to avoid gaps)
            resultRow.push(null);
          }
        }

        // Push the processed row only if it has non-null cells
        result.push(resultRow.filter((cell) => cell !== null));
      }

      return result;
    },
  },
  methods: {
    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const data = await file.arrayBuffer();
      const workbook = XLSX.read(data);
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];

      // Extract values
      this.tableData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

      // Extract merge information
      this.mergeInfo = worksheet["!merges"] || [];

      // Calculate column widths after the table data is set
      this.$nextTick(this.calculateColumnWidths);
    },
    isMergedCell(rowIndex, cellIndex) {
      // Check if a cell is within a merged range
      return this.mergeInfo.some(
        (merge) =>
          rowIndex >= merge.s.r &&
          rowIndex <= merge.e.r &&
          cellIndex >= merge.s.c &&
          cellIndex <= merge.e.c
      );
    },
    isTopLeftOfMergedCell(rowIndex, cellIndex) {
      // Check if this cell is the top-left of a merged region
      return this.mergeInfo.some(
        (merge) => merge.s.r === rowIndex && merge.s.c === cellIndex
      );
    },
    getColspan(rowIndex, cellIndex) {
      // Check if this cell starts a merged region and calculate colspan
      const merge = this.mergeInfo.find(
        (merge) => merge.s.r === rowIndex && merge.s.c === cellIndex
      );
      return merge ? merge.e.c - merge.s.c + 1 : 1;
    },
    getRowspan(rowIndex, cellIndex) {
      // Check if this cell starts a merged region and calculate rowspan
      const merge = this.mergeInfo.find(
        (merge) => merge.s.r === rowIndex && merge.s.c === cellIndex
      );
      return merge ? merge.e.r - merge.s.r + 1 : 1;
    },
    cellStyles(rowIndex, cellIndex, cell, rowspan, colspan) {
      // Define cell styles based on the value type
      const baseStyles = {
        padding: "8px",
        textAlign: typeof cell === "number" ? "right" : "left", // Align right for numbers, left for strings
        whiteSpace: "nowrap", // Prevent wrapping
        overflow: "hidden", // Hide overflow
      };

      if (rowIndex === 0) {
        if (this.firstRowSpan < rowspan) this.firstRowSpan = rowspan;
      }

      if (rowIndex < this.firstRowSpan) {
        return {
          ...baseStyles,
          backgroundColor: "#BDD7EE", // Set the background color to blue
          color: "black", // Optional: change text color to white for better contrast
          fontWeight: "600",
          textAlign: "center",
        };
      }

      if (cellIndex === 0) {
        return { ...baseStyles, fontWeight: "600", textAlign: "center" };
      }

      return baseStyles; // Return default styles for other rows
    },
    formatCellValue(value) {
      // Format numbers with commas and keep strings as they are
      if (typeof value === "number") {
        return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      }
      return value; // Return string value as is
    },
    calculateColumnWidths() {
      const table = this.$refs.excelTable;
      if (!table) return;

      const rows = table.querySelectorAll("tr");
      const widths = [];

      rows.forEach((row) => {
        const cells = row.querySelectorAll("td");

        cells.forEach((cell, index) => {
          const cellWidth = cell.offsetWidth;

          // Update the width if it's the largest found
          if (!widths[index] || cellWidth > widths[index]) {
            widths[index] = cellWidth;
          }
        });
      });

      this.columnWidths = widths; // Update the column widths state
    },
  },
};
</script>

<style scoped>
.excel-table-container {
  margin: 20px;
}
.styled-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto; /* Use auto layout to allow dynamic width */
}
.styled-table th,
.styled-table td {
  border: 2px solid #181717;
}
</style>
