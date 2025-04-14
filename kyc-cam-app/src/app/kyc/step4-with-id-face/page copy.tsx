'use client'
import React, { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'

const Step3IdFace = () => {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [stream, setStream] = useState<MediaStream | null>(null)
  const router = useRouter()

  useEffect(() => {
    const startCamera = async () => {
      try {
        const media = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'user' }, // กล้องหน้า
        })
        if (videoRef.current) {
          videoRef.current.srcObject = media
        }
        setStream(media)
      } catch (err) {
        console.error('❌ เปิดกล้องไม่ได้', err)
      }
    }
    startCamera()
    return () => {
      stream?.getTracks().forEach((track) => track.stop())
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
      formData.append('file', blob, `with_id_${Date.now()}.jpg`)
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })

      if (res.ok) {
        stream?.getTracks().forEach((track) => track.stop())
        alert('📤 ส่งข้อมูลเรียบร้อยแล้ว')
      } else {
        alert('❌ อัปโหลดไม่สำเร็จ')
      }
    }, 'image/jpeg')
  }

  return (
    <div style={{ textAlign: 'center', padding: '1rem' }}>
      <h2>📸 ถ่ายภาพหน้าพร้อมถือบัตร</h2>
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          style={{ width: '100%', maxWidth: 480, borderRadius: 10 }}
        />
        {/* วงรีใบหน้า + สี่เหลี่ยมตำแหน่งบัตร */}
        <div
          style={{
            position: 'absolute',
            border: '3px dashed #00FF00',
            top: '15%',
            left: '25%',
            width: '50%',
            height: '35%',
            borderRadius: '50% / 60%',
            pointerEvents: 'none',
          }}
        />
        <div
          style={{
            position: 'absolute',
            border: '2px dashed orange',
            top: '60%',
            left: '25%',
            width: '50%',
            height: '20%',
            borderRadius: '10px',
            pointerEvents: 'none',
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
          📸 ถ่ายภาพถือบัตร
        </button>
      </div>
    </div>
  )
}

export default Step3IdFace
