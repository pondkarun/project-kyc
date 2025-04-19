import { Client } from 'pg';
import { NextRequest, NextResponse } from 'next/server';

export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
  try {
    const id = params.id;
    const body = await req.json();
    const client = new Client({
      user: 'kyc_user',
      password: 'kyc_pass',
      host: 'localhost',
      port: 5432,
      database: 'kyc_db',
    });
    await client.connect();
    // สมมุติว่าจะ update ฟิลด์ status กับ remark
    const { rowCount } = await client.query(
      `UPDATE kyc_requests SET result = $2 WHERE kyc_id = $1`,
      [id, body]
    );

    await client.end();

    if (rowCount === 0) {
      return NextResponse.json({ error: 'Not Found' }, { status: 404 });
    }

    return NextResponse.json({ message: `อัปเดตข้อมูลสำหรับ id ${id} เรียบร้อย` });
  } catch (error) {
    console.error('Error updating kyc_requests:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}