import { writeFile, mkdir } from 'fs/promises'
import path from 'path'
import { Client } from 'pg'

export async function PUT(req: Request) {
  const { searchParams } = new URL(req.url)
  const kycId = searchParams.get('id')
  const type = searchParams.get('type')

  if (!kycId || !type) {
    return new Response('Missing id or type', { status: 400 })
  }

  const data = await req.formData()
  const file = data.get('file') as File
  if (!file) return new Response('Missing file', { status: 400 })

  const arrayBuffer = await file.arrayBuffer()
  const buffer = Buffer.from(arrayBuffer)
  const folder = path.join(process.cwd(), 'public/uploads', kycId)
  const filepath = path.join(folder, `${type}.jpg`)

  await mkdir(folder, { recursive: true })
  await writeFile(filepath, buffer)

  const client = new Client({
    user: 'kyc_user',
    password: 'kyc_pass',
    host: 'localhost',
    port: 5432,
    database: 'kyc_db',
  })
  await client.connect()

  await client.query(
    `UPDATE kyc_requests
     SET images = jsonb_set(images, $1, to_jsonb($2::text), true)
     WHERE kyc_id = $3`,
    [`{${type}}`, `uploads/${kycId}/${type}.jpg`, kycId]
  )

  await client.end()

  return new Response('Updated', { status: 200 })
}
