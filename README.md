<template>
  <div>
    <!-- Chỉ render thẻ <iframe> nếu nhận được truseted ticket từ backend -->
    <!-- Thuộc tính src của iframe được gán giá trị động từ biến iframeUrl, tạo URL nhúng Tableau-->
    <iframe
      v-if="ticket"
      :src="iframeUrl"
      width="100%"
      height="800px"
      frameborder="0"
    ></iframe>
  </div>
</template>

<script>

import { getTrustedTicketTableau } from '@/api/department_reports'
export default {
  name: 'TableauEmbed',
  data() {
    return {
      //địa chỉ của tableau server
      tableauUrl: 'http://116.103.228.148',
      //Ban đầu là null. Sau khi gọi API thành công, nó sẽ chứa giá trị trusted ticket từ backend.
      ticket: null,
    };
  },
  computed: {
    //Hàm iframeUrl tạo URL hoàn chỉnh để nhúng Tableau, bao gồm
    iframeUrl() {
      // Tạo URL với trusted ticket
      // return ${this.tableauUrl}?trusted_ticket=${this.ticket};
      // if (this.ticket) {
      //   return ${this.tableauUrl}?:embed=yes&:ticket=${this.ticket};
      // } else {
      //   return ${this.tableauUrl}?:embed=yes;
      // }
      // return `${this.tableauUrl}/trusted/${this.ticket}/views/VTG_REPORT_300524/BC04_LCN_TH?embed=y&showTabs=no&showToolbar=no`;


      //trusted/${this.ticket}: Đường dẫn với trusted ticket.
      //views/VTG_REPORT_ALL_IN_ONE/Sheet1: Đường dẫn cụ thể đến báo cáo hoặc sheet.
      /* Query parameters:
      embed=y: Nhúng trực tiếp, không hiển thị giao diện ngoài.
      showTabs=no: Ẩn các tab trong báo cáo.
      showToolbar=no: Ẩn thanh công cụ của Tableau. */
	return `${this.tableauUrl}/trusted/${this.ticket}/views/VTG_REPORT_ALL_IN_ONE/Sheet1?embed=y&showTabs=no&showToolbar=no`;
    }
  },
  //Khi component được khởi tạo, nó sẽ gọi hàm loadTableauViz để lấy trusted ticket.
  async mounted() {
    await this.loadTableauViz();
  },
  methods: {
    async loadTableauViz() {
      try {
        //Gửi yêu cầu đến backend qua hàm getTrustedTicketTableau() để lấy trusted ticket.
        const response = await getTrustedTicketTableau();
        //Nếu lấy thành công, gán giá trị trusted ticket vào this.ticket
        if (response && response.data && response.data.ticket) {
          //API trả về response.data.ticket, đây là nơi chứa trusted ticket.
          this.ticket = response.data.ticket;
        } else {
          console.error('Không thể lấy trusted ticket từ Tableau');
        }
      } catch (error) {
        console.error('Lỗi khi gọi API:', err);
        error.value = 'Có lỗi khi gửi yêu cầu đến backend';
      }
    }
  }
}
</script>

<style scoped>
.tableau-container {
  width: 100%;
  height: 600px;
}
</style>
