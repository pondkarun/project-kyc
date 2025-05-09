'use client'

import { Loading3QuartersOutlined, LoadingOutlined } from '@ant-design/icons';
import { Badge, Button, Card, Col, ConfigProvider, Descriptions, Image, Input, message, Modal, Row, Spin, Splitter, Table, TableProps, theme, Watermark } from 'antd'
import dayjs from 'dayjs';
import './page.css';
import { isBoolean } from 'lodash'
import { useEffect, useState } from 'react';

interface DataType {
  kyc_id?: string;
  status: "pending" | "processed" | "done";
  created_at: Date;
  images: {
    face?: string;
    id_back?: string;
    with_id?: string;
    id_front?: string;
  };
  result?: {
    data?: {
      name_en?: string | null;
      name_th?: string | null;
      birth_en?: string | null;
      birth_th?: string | null;
      issue_th?: string | null;
      expiry_th?: string | null;
      id_number?: string | null;
    };
    kyc_data?: {
      kyc_passed?: boolean | null;
      face_scores?: {
        average?: number | null;
        id_vs_selfie?: number | null;
        id_vs_with_id?: number | null;
        selfie_vs_with_id?: number | null;
      }
      admin_data?: {
        admin_passed?: boolean | null;
        admin_comment?: string | null;
        admin_name?: string | null;
        admin_time?: Date | null;
      }
    };
  }
}

const images = { "face": "uploads/1c713ac0-6bbb-437c-b441-6a1d35e29c08/face.jpg", "id_back": "uploads/1c713ac0-6bbb-437c-b441-6a1d35e29c08/id_back.jpg", "with_id": "uploads/1c713ac0-6bbb-437c-b441-6a1d35e29c08/with_id.jpg", "id_front": "uploads/1c713ac0-6bbb-437c-b441-6a1d35e29c08/id_front.jpg" }
const result_0 = { "data": { "name_en": "Kalantabutra", "name_th": null, "birth_en": "17jul1996", "birth_th": "17n..2539", "issue_th": null, "expiry_th": null, "id_number": "10100509171004" }, "kyc_data": { "kyc_passed": true, "face_scores": { "average": 46.57, "id_vs_selfie": 58.06, "id_vs_with_id": 37.97, "selfie_vs_with_id": 43.68 } } }
const result_1 = { "data": { "name_en": "Kalantabutra", "name_th": null, "birth_en": "17jul1996", "birth_th": "17n..2539", "issue_th": null, "expiry_th": null, "id_number": "10100509171004" }, "kyc_data": { "kyc_passed": false, "face_scores": { "average": 46.57, "id_vs_selfie": 58.06, "id_vs_with_id": 37.97, "selfie_vs_with_id": 43.68 } } }
const result_2 = { "data": { "name_en": "Kalantabutra", "name_th": null, "birth_en": "17jul1996", "birth_th": "17n..2539", "issue_th": null, "expiry_th": null, "id_number": "10100509171004" }, "kyc_data": { "kyc_passed": false, "face_scores": { "average": 46.57, "id_vs_selfie": 58.06, "id_vs_with_id": 37.97, "selfie_vs_with_id": 43.68 } } }
const result_3 = { "data": { "name_en": "Kalantabutra", "name_th": null, "birth_en": "17jul1996", "birth_th": "17n..2539", "issue_th": null, "expiry_th": null, "id_number": "10100509171004" }, "kyc_data": { "kyc_passed": false, "face_scores": { "average": 46.57, "id_vs_selfie": 58.06, "id_vs_with_id": 37.97, "selfie_vs_with_id": 43.68 }, "admin_data": { "admin_passed": true, "admin_comment": null, "admin_name": "Admin", "admin_time": null } } }
const result_4 = { "data": { "name_en": "Kalantabutra", "name_th": null, "birth_en": "17jul1996", "birth_th": "17n..2539", "issue_th": null, "expiry_th": null, "id_number": "10100509171004" }, "kyc_data": { "kyc_passed": false, "face_scores": { "average": 46.57, "id_vs_selfie": 58.06, "id_vs_with_id": 37.97, "selfie_vs_with_id": 43.68 }, "admin_data": { "admin_passed": false, "admin_comment": null, "admin_name": "Admin", "admin_time": null } } }

const KycRequestsPage = () => {

  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchKycRequests();
  }, [])

  const fetchKycRequests = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/kyc/kyc-requests');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setLoading(false);
      console.log('Fetched KYC requests:', data);
      setData(data);
    } catch (error) {
      setLoading(false);
      console.error('Error fetching KYC requests:', error);
    }
  };

  const getStatus = (obj: any) => {
    const admin_passed = obj.result?.kyc_data?.admin_data?.admin_passed;
    const kyc_data = obj.result?.kyc_data?.kyc_passed;
    if (obj.status === "processed") {
      return <Spin indicator={<LoadingOutlined spin />} size="small" />
    } else if (admin_passed === true) {
      return <Badge color="green" />
    } else if (admin_passed === false) {
      return <Badge color="red" />
    } else if (kyc_data === true) {
      return <Badge color="green" />
    } else if (kyc_data === false) {
      return <Badge color="yellow" />
    } else {
      return "??"
    }
  }

  const columns: TableProps<DataType>['columns'] = [
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 80,
      align: 'center',
      render: (v, o) => getStatus(o),
    },
    {
      title: 'Created At',
      dataIndex: 'created_at',
      key: 'created_at',
      align: 'center',
      render: (v) => <a>{dayjs(v).format("DD/MM/YYYY HH:mm")}</a>,
    },
  ];

  const [data, setData] = useState<DataType[]>([
    /* {
      status: "processed",
      images,
      created_at: new Date("2023-10-01T12:12:00Z"),
    },
    {
      status: "done",
      images,
      created_at: new Date("2023-10-02T09:22:00Z"),
      result: result_1
    },
    {
      status: "done",
      images,
      created_at: new Date("2023-10-03T13:01:00Z"),
      result: result_2
    },
    {
      status: "done",
      images,
      created_at: new Date("2023-10-04T12:10:00Z"),
      result: result_3
    },
    {
      status: "done",
      images,
      created_at: new Date(),
      result: result_4
    },
    {
      status: "done",
      images,
      created_at: new Date(),
      result: result_0
    }, */
  ])
  const [selectedRowKey, setSelectedRowKey] = useState<number | null>(null);
  const [selectedData, setSelectedData] = useState<DataType | null>(null);


  const approveOrRejectRequest = async (id: string, data: DataType) => {
    if (!selectedData) return;
    try {
      await fetch(`/api/kyc/kyc-requests/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data.result),
      });
      setIsModalOpen(false);
      setSelectedRowKey(null);
      setSelectedData(null);
      setStatus(undefined);
      message.success('อนุมัติเรียบร้อย');
      // Refresh the KYC requests after approval
      fetchKycRequests();
    } catch (error) {
      console.error('Error approving request:', error);
    }
  };


  const [status, setStatus] = useState<boolean | undefined>(undefined)

  const approveRequest = async (data: DataType) => {
    setIsModalOpen(true);
    setStatus(true)
  }

  const rejectRequest = async (data: DataType) => {
    setIsModalOpen(true);
    setStatus(false)
  }

  const onOkApproveRejectRequest = async (data: DataType) => {
    const obj: DataType = { ...data }
    if (obj.result?.kyc_data?.admin_data) {
      obj.result.kyc_data.admin_data = {
        ...obj.result.kyc_data.admin_data,
        admin_passed: status,
        admin_time: new Date(),
        admin_name: "Admin",
      }
      if (obj.kyc_id) {
        setIsModalOpen(false);
        approveOrRejectRequest(obj.kyc_id, obj)
      }
    }
  }

  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    if (loading == true) {
      setSelectedRowKey(null);
      setSelectedData(null);
    }
  }, [loading])

  return (
    <ConfigProvider theme={{ algorithm: theme.darkAlgorithm, token: { fontFamily: "'Kanit', sans-serif" } }}>
      <Card size="default" title="KYC" style={{ width: "100%" }}>

        <Splitter>
          <Splitter.Panel defaultSize="20%" min="20%" max="70%" style={{ padding: "20px" }}>
            <Button
              onClick={() => {
                fetchKycRequests();
              }}
              style={{
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer',
                marginBottom: '20px',
              }}
            >
              <Loading3QuartersOutlined style={{ marginRight: '5px' }} />
              Refresh
            </Button>

            <Table<DataType>
              loading={loading}
              columns={columns}
              dataSource={data}
              rowKey={(record, index: any) => index}
              onRow={(record, index) => ({
                onClick: () => {
                  setSelectedRowKey(index ?? null);
                  setSelectedData(record);
                },
              })}
              rowClassName={(_, index) => (index === selectedRowKey ? 'active-row' : '')}
            />
          </Splitter.Panel>
          <Splitter.Panel style={{ padding: "20px" }}>
            {selectedData ? selectedData.status == "processed" ? <div style={{ color: 'white' }}>ระบบกำลังประมวลผล</div> :
              (
                <>
                  <Row gutter={[16, 0]}>
                    <Col span={12}>
                      <Descriptions title="OCR Result" bordered column={1} size="small">
                        <Descriptions.Item label="เลขที่บัตรประชาชน">{selectedData.result?.data?.id_number}</Descriptions.Item>
                        <Descriptions.Item label="ชื่อไทย">{selectedData.result?.data?.name_th}</Descriptions.Item>
                        <Descriptions.Item label="ชื่ออังกฤษ">{selectedData.result?.data?.name_en}</Descriptions.Item>
                        <Descriptions.Item label="วันเกิดไทย">{selectedData.result?.data?.birth_th}</Descriptions.Item>
                        <Descriptions.Item label="วันเกิดอังกฤษ">{selectedData.result?.data?.birth_en}</Descriptions.Item>
                      </Descriptions>
                    </Col>
                    <Col span={12}>
                      <Descriptions title="ผลการตรวจสอบ KYC" bordered column={1} size="small">
                        <Descriptions.Item label="ผลการตรวจสอบ KYC">{selectedData.result?.kyc_data?.kyc_passed ? "ผ่าน" : "ไม่ผ่าน"}</Descriptions.Item>
                        <Descriptions.Item label="คะแนนเฉลี่ย">{selectedData.result?.kyc_data?.face_scores?.average}%</Descriptions.Item>
                        <Descriptions.Item label="คะแนน บัตรประชาชน vs หน้า">{selectedData.result?.kyc_data?.face_scores?.id_vs_selfie}%</Descriptions.Item>
                        <Descriptions.Item label="คะแนน บัตรประชาชน vs หน้าถือบัตร">{selectedData.result?.kyc_data?.face_scores?.id_vs_with_id}%</Descriptions.Item>
                        <Descriptions.Item label="คะแนน หน้า vs หน้าถือบัตร">{selectedData.result?.kyc_data?.face_scores?.selfie_vs_with_id}%</Descriptions.Item>
                      </Descriptions>
                    </Col>
                  </Row>

                  {selectedData.result?.kyc_data?.kyc_passed ? null : selectedData.result?.kyc_data?.admin_data && isBoolean(selectedData.result?.kyc_data?.admin_data?.admin_passed) ? (
                    <div style={{ marginTop: '20px' }}>
                      <Descriptions title="Admin" bordered column={1} size="small">
                        <Descriptions.Item label="ผลการตรวจสอบ Admin">{selectedData.result?.kyc_data?.admin_data?.admin_passed ? "ผ่าน" : "ไม่ผ่าน"}</Descriptions.Item>
                        <Descriptions.Item label="ชื่อ Admin">{selectedData.result?.kyc_data?.admin_data?.admin_name}</Descriptions.Item>
                        <Descriptions.Item label="ความคิดเห็น Admin">{selectedData.result?.kyc_data?.admin_data?.admin_comment}</Descriptions.Item>
                        <Descriptions.Item label="วันเวลาที่ตรวจสอบ Admin">{selectedData.result?.kyc_data?.admin_data?.admin_time && dayjs(selectedData.result?.kyc_data?.admin_data?.admin_time).format("DD/MM/YYYY HH:mm")}</Descriptions.Item>
                      </Descriptions>
                    </div>
                  ) : (
                    <div style={{ marginTop: '20px' }}>
                      <Row gutter={16}>
                        <Col>
                          <Button onClick={() => approveRequest({ ...selectedData })} style={{ backgroundColor: '#52c41a', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}>
                            อนุมัติ
                          </Button>
                        </Col>
                        <Col>
                          <Button onClick={() => rejectRequest({ ...selectedData })} style={{ backgroundColor: '#f5222d', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}>
                            ไม่อนุมัติ
                          </Button>

                          <Modal
                            title="ยืนยันการ อนุมัติ/ไม่อนุมัติ"
                            open={isModalOpen}
                            onOk={() => onOkApproveRejectRequest({ ...selectedData })}
                            onCancel={() => setIsModalOpen(false)}
                            okText="ยืนยัน"
                            cancelText="ยกเลิก"
                          >
                            <Input.TextArea
                              rows={10}
                              placeholder="ความคิดเห็น"
                              value={selectedData.result?.kyc_data?.admin_data?.admin_comment ?? ""}
                              onChange={(e) => {
                                if (!selectedData || !selectedData.result || !selectedData.result.kyc_data) return;
                                setSelectedData({
                                  ...selectedData,
                                  result: {
                                    ...selectedData.result,
                                    kyc_data: {
                                      ...selectedData.result.kyc_data,
                                      admin_data: {
                                        ...(selectedData.result.kyc_data.admin_data ?? {}),
                                        admin_comment: e.target.value,
                                      },
                                    },
                                  },
                                });
                              }}
                            />
                          </Modal>
                        </Col>
                      </Row>
                    </div>
                  )}

                  <div style={{ marginTop: "20px", backgroundColor: "rgb(48, 48, 48)", padding: "20px", borderRadius: "10px" }}>
                    <Row gutter={16}>
                      <Col span={6}>
                        <ImageKYC src={selectedData.images.face} text="รูปหน้า" obj={selectedData.images} />
                      </Col>
                      <Col span={6}>
                        <ImageKYC src={selectedData.images.id_front} text="รูปหน้าบัตรประชาชน" obj={selectedData.images} />
                      </Col>
                      <Col span={6}>
                        <ImageKYC src={selectedData.images.id_back} text="รูปหลังบัตรประชาชน" obj={selectedData.images} />
                      </Col>
                      <Col span={6}>
                        <ImageKYC src={selectedData.images.with_id} text="รูปหน้ากับบัตรประชาชน" obj={selectedData.images} />
                      </Col>
                    </Row>
                  </div>
                </>
              ) : (
              <div style={{ color: 'white' }}>กรุณาเลือกข้อมูลจากตาราง</div>
            )}
          </Splitter.Panel>
        </Splitter>
      </Card>
    </ConfigProvider >
  )
}

const ImageKYC = ({ src, text, obj }: any) => {
  return (
    <Watermark content="ใช้สำหรบทำวิจัยเท่านั้น" style={{ width: "100%", height: "100%" }}>
      <Card
        variant="borderless"
        style={{ width: "100%", textAlign: "center" }}
        cover={
          <Image.PreviewGroup
            items={[
              `/${obj.face}`,
              `/${obj.id_back}`,
              `/${obj.id_front}`,
              `/${obj.with_id}`,
            ]}
          >
            <Image
              src={`/${src}`}
              alt={text}
            />
          </Image.PreviewGroup>
        }
      >
        <h2>{text}</h2>
      </Card>
    </Watermark>
  )
}

export default KycRequestsPage