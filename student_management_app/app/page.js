"use client";

import { useEffect, useState } from "react";

const HomePage = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStudentsData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/students`);
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }

        const data = await response.json();
        console.log("Fetched Data:", data); // Add a console log here to see the actual data
        setData(data?.student_data || []); // Ensure the key matches the API response
      } catch (error) {
        setError("Error fetching data.");
        console.log("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStudentsData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <>
      <h2 className="text-2xl font-semibold text-center mt-8">Home Page</h2>
      <div className="container mx-auto mt-8">
        <div className="overflow-x-auto">
          <table className="min-w-full table-auto border-collapse border border-gray-300">
            <thead className="bg-gray-200 text-blue-700">
              <tr>
                <th className="border border-blue-300 px-4 py-2">Student ID</th>
                <th className="border border-blue-300 px-4 py-2">First Name</th>
                <th className="border border-blue-300 px-4 py-2">Last Name</th>
                <th className="border border-blue-300 px-4 py-2">Gender</th>
                <th className="border border-blue-300 px-4 py-2">Email</th>
                <th className="border border-blue-300 px-4 py-2">
                  Father's Name
                </th>
                <th className="border border-blue-300 px-4 py-2">
                  Date of Birth
                </th>
                <th className="border border-blue-300 px-4 py-2">Grade</th>
                <th className="border border-blue-300 px-4 py-2">Phone</th>
              </tr>
            </thead>
            <tbody className="text-sm text-gray-700">
              {Array.isArray(data) && data.length > 0 ? (
                data.map((student, index) => (
                  <tr key={index} className="hover:bg-blue-100">
                    <td className="border border-blue-300 px-4 py-2">
                      {student.student_id}
                    </td>
                    <td className="border border-blue-300 px-4 py-2">
                      {student.first_name}
                    </td>
                    <td className="border border-blue-300 px-4 py-2">
                      {student.last_name}
                    </td>
                    <td className="border border-blue-300 px-4 py-2">
                      {student.gender}
                    </td>
                    <td className="border border-blue-300 px-4 py-2">
                      {student.email}
                    </td>
                    <td className="border border-blue-300 px-4 py-2">
                      {student.father_name}
                    </td>
                    <td className="border border-blue-300 px-4 py-2">
                      {student.date_of_birth}
                    </td>
                    <td className="border border-blue-300 px-4 py-2">
                      {student.grade}
                    </td>
                    <td className="border border-blue-300 px-4 py-2">
                      {student.phone}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan="9"
                    className="border border-blue-300 px-4 py-2 text-center"
                  >
                    No students found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
};

export default HomePage;
