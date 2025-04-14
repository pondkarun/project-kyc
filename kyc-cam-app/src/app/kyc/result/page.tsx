'use client'

import { ConfigProvider, Result, theme } from 'antd'
import React from 'react'

const KycResult = () => {
  return (
    <ConfigProvider theme={{ algorithm: theme.darkAlgorithm }}>
      <Result
        status="info"
        title="อยู่ระหว่างตรวจสอบข้อมูล KYC"
        subTitle="ระบบกำลังประมวลผลข้อมูลของคุณ กรุณารอสักครู่"
      />
    </ConfigProvider>
  )
}

export default KycResult