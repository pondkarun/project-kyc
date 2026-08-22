'use client'
import React, { useEffect, useRef, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'

const COUNTDOWN_SECONDS = 5

const Step4WithIdFace = () => {
  const videoRef = useRef<HTMLVideoElement | null>(null)
  const router = useRouter()
  const { kyc_id } = useParams()
  const [countdown, setCountdown] = useState<number | null>(null)

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user' }
    })
    if (videoRef.current) {
      videoRef.current.srcObject = stream
    }
  }

  const handleCapture = () => {
    if (!videoRef.current) return
    const canvas = document.createElement('canvas')
    canvas.width = videoRef.current.videoWidth
    canvas.height = videoRef.current.videoHeight
    const ctx = canvas.getContext('2d')
    if (ctx) {
      ctx.drawImage(videoRef.current, 0, 0)
      canvas.toBlob(async (blob) => {
        if (!blob) return
        const formData = new FormData()
        formData.append('file', blob, 'with_id.jpg')
        await fetch(`/api/kyc/update?id=${kyc_id}&type=with_id`, {
          method: 'PUT',
          body: formData,
        })
        const stream = videoRef.current!.srcObject as MediaStream
        stream.getTracks().forEach(track => track.stop())
        router.push(`/kyc/result`)
      }, 'image/jpeg')
    }
  }

  const startCountdown = () => {
    setCountdown(COUNTDOWN_SECONDS)
  }

  useEffect(() => {
    if (countdown === null) return
    if (countdown === 0) {
      handleCapture()
      return
    }
    const timer = setTimeout(() => setCountdown(countdown - 1), 1000)
    return () => clearTimeout(timer)
  }, [countdown])

  useEffect(() => {
    startCamera()
  }, [])

  return (
    <div style={{ textAlign: 'center', padding: '1rem' }}>
      <h2>📸 ถ่ายภาพหน้าพร้อมถือบัตร</h2>
      <p style={{ maxWidth: 480, margin: '0 auto 1rem', color: '#555' }}>
        กดปุ่ม &ldquo;เริ่มนับถอยหลัง&rdquo; ก่อน แล้วค่อยยกบัตรขึ้นถือคู่กับใบหน้า ให้เห็นทั้งใบหน้าและบัตรอยู่ในกรอบมุมทั้ง 4 (ไม่ต้องเป๊ะ แค่อยู่ในกรอบก็พอ) ภายใน {COUNTDOWN_SECONDS} วินาที ระบบจะถ่ายภาพให้อัตโนมัติ ไม่ต้องกดถ่ายเองพร้อมถือบัตร
      </p>
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <img
          src="/overlay/with-id-overlay.png"
          alt="overlay"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
            zIndex: 10,
          }}
        />
        <video ref={videoRef} autoPlay playsInline muted style={{ width: '100%', maxWidth: 480 }} />
        {countdown !== null && countdown > 0 && (
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '5rem',
              fontWeight: 'bold',
              color: '#fff',
              textShadow: '0 0 12px rgba(0,0,0,0.8)',
              zIndex: 20,
              pointerEvents: 'none',
            }}
          >
            {countdown}
          </div>
        )}
      </div>
      <div style={{ marginTop: '1rem' }}>
        <button
          onClick={startCountdown}
          disabled={countdown !== null}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: countdown !== null ? '#999' : '#0070f3',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: countdown !== null ? 'default' : 'pointer',
          }}
        >
          {countdown !== null ? `กำลังนับถอยหลัง... ${countdown}` : '⏱️ เริ่มนับถอยหลัง'}
        </button>
      </div>
    </div>
  )
}

export default Step4WithIdFace
