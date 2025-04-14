import { writeFile, mkdir } from 'fs/promises'
import path from 'path'
import { Client } from 'pg'

export async function POST(req: Request) {
  const data = await req.formData()
  const kycId = data.get('id')?.toString()
  if (!kycId) return Response.json({ error: 'Missing ID' }, { status: 400 })
  const folder = path.join(process.cwd(), 'public/uploads', kycId)

  await mkdir(folder, { recursive: true })

  const files = ['face', 'id_front', 'id_back', 'with_id']
  const imagePaths: Record<string, string> = {}

  for (const field of files) {
    const file = data.get(field) as File
    if (file) {
      const arrayBuffer = await file.arrayBuffer()
      const buffer = Buffer.from(arrayBuffer)
      const savePath = path.join(folder, `${field}.jpg`)
      await writeFile(savePath, buffer)
      imagePaths[field] = `uploads/${kycId}/${field}.jpg`
    }
  }

  const saveKycToDb = async (kycId: string, images: Record<string, string>) => {
    const client = new Client({
      user: 'kyc_user',
      password: 'kyc_pass',
      host: 'localhost',
      port: 5432,
      database: 'kyc_db',
    })
    await client.connect()

    await client.query(`
      INSERT INTO kyc_requests (kyc_id, images, created_at, status, result)
      VALUES ($1, $2, NOW(), 'pending', NULL)
    `, [kycId, images])

    await client.end()
  }

  await saveKycToDb(kycId, imagePaths)

  return Response.json({ success: true, kyc_id: kycId })
}