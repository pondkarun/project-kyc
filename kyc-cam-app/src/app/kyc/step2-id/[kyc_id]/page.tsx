'use client'
import React, { useEffect, useRef, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'

const Step2IdFront = () => {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [stream, setStream] = useState<MediaStream | null>(null)
  const router = useRouter()
  const { kyc_id }: { kyc_id: string } = useParams()

  useEffect(() => {
    const startCamera = async () => {
      try {
        const media = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { exact: 'environment' } }
        })
        if (videoRef.current) {
          videoRef.current.srcObject = media
        }
        setStream(media)
      } catch (err) {
        // fallback to default camera
        const media = await navigator.mediaDevices.getUserMedia({ video: true })
        if (videoRef.current) {
          videoRef.current.srcObject = media
        }
        setStream(media)
      }
    }
    startCamera()

    return () => {
      stream?.getTracks().forEach(track => track.stop())
    }
  }, [])

  const handleCapture = async () => {
    if (!videoRef.current || !canvasRef.current) return

    const context = canvasRef.current.getContext('2d')
    if (!context) return

    const width = videoRef.current.videoWidth
    const height = videoRef.current.videoHeight
    canvasRef.current.width = width
    canvasRef.current.height = height

    context.drawImage(videoRef.current, 0, 0, width, height)
    canvasRef.current.toBlob(async (blob) => {
      if (!blob) return
      const formData = new FormData()
      formData.append('file', blob, 'id_front.jpg')

      await fetch(`/api/kyc/update?id=${kyc_id}&type=id_front`, {
        method: 'PUT',
        body: formData,
      })

      stream?.getTracks().forEach(track => track.stop())
      router.push(`/kyc/step3-id-back/${kyc_id}`)
    }, 'image/jpeg')
  }

  return (
    <div style={{ textAlign: 'center', padding: '1rem' }}>
      <h2>📷 ถ่ายรูปบัตรประชาชนด้านหน้า</h2>
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          style={{ width: '100%', maxWidth: 480, borderRadius: 10 }}
        />
        <img
          src="/overlay/font_id.png"
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
        <canvas ref={canvasRef} style={{ display: 'none' }} />
      </div>
      <div style={{ marginTop: '1rem' }}>
        <button
          onClick={handleCapture}
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

export default Step2IdFront