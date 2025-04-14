'use client'

// imports ด้านบน
import * as faceapi from 'face-api.js'
import { useEffect, useRef, useState } from 'react'

export default function EyeCheck() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [status, setStatus] = useState<string>('⏳ กำลังโหลดกล้อง...')
  const [passedTime, setPassedTime] = useState<number>(0)
  const [captured, setCaptured] = useState<boolean>(false)

  useEffect(() => {
    const loadModels = async () => {
      const MODEL_URL = '/models'
      await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL)
      await faceapi.nets.faceLandmark68TinyNet.loadFromUri(MODEL_URL)
      await faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL)
      await faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL)
    }

    const startVideo = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }
    }

    loadModels().then(startVideo)
  }, [])

  useEffect(() => {
    const interval = setInterval(detectEyes, 300)
    return () => clearInterval(interval)
  }, [])

  const detectEyes = async () => {
    if (!videoRef.current) return

    const detection = await faceapi
      .detectSingleFace(videoRef.current, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks(true) // ✅ ใช้ true เพื่อ match กับ TinyNet

    if (!detection) {
      setStatus('❌ ไม่พบใบหน้า')
      return
    }

    // ตรวจว่าหน้าอยู่ในวงรีกลางจอหรือไม่
    const box = detection.detection.box
    const overlayCenterX = videoRef.current!.videoWidth / 2
    const overlayCenterY = videoRef.current!.videoHeight / 2
    const ellipseWidth = 180
    const ellipseHeight = 240

    const faceCenterX = box.x + box.width / 2
    const faceCenterY = box.y + box.height / 2

    const normX = (faceCenterX - overlayCenterX) / (ellipseWidth / 2)
    const normY = (faceCenterY - overlayCenterY) / (ellipseHeight / 2)
    const inEllipse = (normX ** 2 + normY ** 2) <= 1

    const faceWidthThreshold = ellipseWidth * 0.7
    const faceHeightThreshold = ellipseHeight * 0.7
    if (box.width < faceWidthThreshold || box.height < faceHeightThreshold) {
      setStatus('❌ โปรดยื่นหน้าให้เต็มวงรี')
      return
    }

    if (!inEllipse) {
      setStatus('❌ โปรดย้ายหน้าให้อยู่ในวงรี')
      return
    }

    const landmarks = detection.landmarks
    const leftEye = landmarks.getLeftEye()
    const rightEye = landmarks.getRightEye()

    if (isEyeClosed(leftEye) && isEyeClosed(rightEye)) {
      setStatus('❌ หลับตาหรือไม่พบตา')
    } else {
      setStatus('✅ ลืมตาแล้ว')
    }
  }

  const isEyeClosed = (eye: faceapi.Point[]) => {
    const vertical1 = distance(eye[1], eye[5])
    const vertical2 = distance(eye[2], eye[4])
    const horizontal = distance(eye[0], eye[3])
    const ratio = (vertical1 + vertical2) / (2.0 * horizontal)
    return ratio < 0.25 // 👁️ threshold นี้คุณสามารถปรับได้
  }

  const distance = (p1: faceapi.Point, p2: faceapi.Point) => {
    return Math.hypot(p1.x - p2.x, p1.y - p2.y)
  }

  useEffect(() => {
    let timer: NodeJS.Timeout
    if (status === '✅ ลืมตาแล้ว') {
      timer = setInterval(() => {
        setPassedTime(prev => {
          if (prev >= 3 && !captured) {
            captureImage()
            setCaptured(true)
            clearInterval(timer)
            return 0
          }
          return prev + 1
        })
      }, 1000)
    } else {
      setPassedTime(0)
      setCaptured(false)
    }
    return () => clearInterval(timer)
  }, [status])

  const captureImage = () => {
    if (!videoRef.current) return
    const canvas = document.createElement('canvas')
    canvas.width = videoRef.current.videoWidth
    canvas.height = videoRef.current.videoHeight
    const ctx = canvas.getContext('2d')
    if (ctx) {
      ctx.drawImage(videoRef.current, 0, 0)
      const dataUrl = canvas.toDataURL('image/jpeg')
      console.log('📸 รูปถูกบันทึก:', dataUrl)

      // สร้างลิงก์ดาวน์โหลด
      const link = document.createElement('a')
      link.href = dataUrl
      link.download = 'kyc_snapshot.jpg'
      link.click()
    }
  }

  return (
    <div style={{ textAlign: 'center', padding: '2rem' }}>
      <h2>👁️ ตรวจว่าลืมตาหรือไม่</h2>
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <video ref={videoRef} autoPlay muted playsInline width={480} height={640} style={{ borderRadius: 12 }} />
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          width: 180,
          height: 240,
          transform: 'translate(-50%, -50%)',
          border: '3px dashed lime',
          borderRadius: '50% / 60%',
          zIndex: 10,
          pointerEvents: 'none'
        }} />
      </div>
      <p style={{ fontSize: '1.25rem', marginTop: '1rem', color: status.includes('✅') ? 'green' : 'red' }}>
        {status} {status.includes('✅') && !captured ? `⏳ (${3 - passedTime})` : ''}
      </p>
    </div>
  )
}