<template>
  <div class="dashboard__help">
    <img src="@baserow/modules/core/static/img/vocabai_banner.png" alt="" style="height: 80px;"/>
    <p class="dashboard__help-description">
      Introducing <b>Vocab.Ai</b> - The revolutionary language learning spreadsheet designed to supercharge your vocabulary and sentence mastery!
      <br/>
      Need help ? <a href="https://lucw.medium.com/unlock-the-power-of-pinyin-vocab-ais-edc5db83a1a9" target="_blank">Chinese and Pinyin tutorial</a>
      <br/>
      <i>note: Vocab.Ai is based on open-source database <a href="https://baserow.io" target="_blank">Baserow</a></i>
    </p>
  </div>
</template>

<script>
const helpDisplayCookieName = 'baserow_dashboard_alert_closed'

export default {
  name: 'DashboardHelp',
  data() {
    return {
      showAlert: true,
    }
  },
  computed: {
    displayAlert() {
      return this.showAlert && !this.$cookies.get(helpDisplayCookieName)
    },
  },
  methods: {
    handleAlertClose() {
      this.showAlert = false
      this.$cookies.set(helpDisplayCookieName, true, {
        path: '/',
        maxAge: 60 * 60 * 24 * 182, // 6 months
      })
    },
  },
}
</script>
