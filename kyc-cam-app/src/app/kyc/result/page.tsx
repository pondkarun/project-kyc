'use client'

import { Result } from 'antd'
import React from 'react'

const KycResult = () => {
  return (
    <Result
      status="info"
      title="อยู่ระหว่างตรวจสอบข้อมูล KYC"
      subTitle="ระบบกำลังประมวลผลข้อมูลของคุณ กรุณารอสักครู่"
    />
  )
}

export default KycResult