import { Client } from 'pg';
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const client = new Client({
      user: 'kyc_user',
      password: 'kyc_pass',
      host: 'localhost',
      port: 5432,
      database: 'kyc_db',
    })
    await client.connect()

    const { rows } = await client.query(
      `SELECT * FROM kyc_requests WHERE status IN ($1, $2)`,
      ['done', 'processed']
    )

    await client.end()
    return NextResponse.json(rows);
  } catch (error) {
    console.error('Error fetching kyc_requests:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
