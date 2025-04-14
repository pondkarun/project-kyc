'use client'

import { useEffect, useRef } from 'react'
import { useRouter, useParams } from 'next/navigation'

const Step3IdBack = () => {
  const videoRef = useRef<HTMLVideoElement | null>(null)
  const router = useRouter()
  const { kyc_id } = useParams()

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { exact: 'environment' } }
    })
    if (videoRef.current) {
      videoRef.current.srcObject = stream
    }
  }

  const captureImage = () => {
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
        formData.append('file', blob, 'id_back.jpg')
        await fetch(`/api/kyc/update?id=${kyc_id}&type=id_back`, {
          method: 'PUT',
          body: formData,
        })
        const stream = videoRef.current!.srcObject as MediaStream
        stream.getTracks().forEach(track => track.stop())
        router.push(`/kyc/step4-with-id-face/${kyc_id}`)
      }, 'image/jpeg')
    }
  }

  useEffect(() => {
    startCamera()
  }, [])

  return (
    <div style={{ textAlign: 'center', padding: '1rem' }}>
      <h2>📷 ถ่ายรูปบัตรประชาชนด้านหลัง</h2>
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <video ref={videoRef} autoPlay playsInline muted style={{ width: '100%', maxWidth: 480 }} />
        <img
          src="/overlay/back_id.png"
          alt="overlay"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            pointerEvents: 'none',
            zIndex: 10,
          }}
        />
      </div>
      <div style={{ marginTop: '1rem' }}>
        <button
          onClick={captureImage}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: '#0070f3',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
          }}
        >
          📸 ถ่ายรูปบัตร
        </button>
      </div>
    </div>
  )
}

export default Step3IdBack