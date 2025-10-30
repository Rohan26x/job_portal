'use client';

import { useState, useEffect } from 'react';
import { resumeAPI } from '@/lib/api';
import styles from './Resume.module.css';

export default function ResumePage() {
  const [resume, setResume] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const [formData, setFormData] = useState({
    about_me: '',
    skills: [{ skill_name: '' }],
    education: [{ school_name: '', degree: '', field_of_study: '' }],
    certifications: [{ cert_name: '', issuing_organization: '' }],
  });

  useEffect(() => {
    fetchResume();
  }, []);

  const fetchResume = async () => {
    try {
      const response = await resumeAPI.getMyResume();
      setResume(response.data);

      setFormData({
        about_me: response.data.about_me || '',
        skills: response.data.resume_skills?.length > 0
          ? response.data.resume_skills.map(rs => ({ skill_name: rs.skill.skill_name }))
          : [{ skill_name: '' }],
        education: response.data.educations?.length > 0
          ? response.data.educations
          : [{ school_name: '', degree: '', field_of_study: '' }],
        certifications: response.data.certifications?.length > 0
          ? response.data.certifications
          : [{ cert_name: '', issuing_organization: '' }],
      });
    } catch (error) {
      if (error.response?.status === 404) {
        console.log('No resume found, user can create one');
        setIsEditing(true);
      } else {
        console.error('Error fetching resume:', error);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Skills management
  const addSkill = () => {
    setFormData({
      ...formData,
      skills: [...formData.skills, { skill_name: '' }],
    });
  };

  const removeSkill = (index) => {
    const newSkills = formData.skills.filter((_, i) => i !== index);
    setFormData({ ...formData, skills: newSkills });
  };

  const updateSkill = (index, value) => {
    const newSkills = [...formData.skills];
    newSkills[index].skill_name = value;
    setFormData({ ...formData, skills: newSkills });
  };

  // Education management
  const addEducation = () => {
    setFormData({
      ...formData,
      education: [...formData.education, { school_name: '', degree: '', field_of_study: '' }],
    });
  };

  const removeEducation = (index) => {
    const newEducation = formData.education.filter((_, i) => i !== index);
    setFormData({ ...formData, education: newEducation });
  };

  const updateEducation = (index, field, value) => {
    const newEducation = [...formData.education];
    newEducation[index][field] = value;
    setFormData({ ...formData, education: newEducation });
  };

  // Certifications management
  const addCertification = () => {
    setFormData({
      ...formData,
      certifications: [...formData.certifications, { cert_name: '', issuing_organization: '' }],
    });
  };

  const removeCertification = (index) => {
    const newCerts = formData.certifications.filter((_, i) => i !== index);
    setFormData({ ...formData, certifications: newCerts });
  };

  const updateCertification = (index, field, value) => {
    const newCerts = [...formData.certifications];
    newCerts[index][field] = value;
    setFormData({ ...formData, certifications: newCerts });
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');

    try {
      const payload = {
        about_me: formData.about_me,
        skills: formData.skills.filter(s => s.skill_name.trim() !== '').map(s => s.skill_name),
        education: formData.education.filter(e => e.school_name.trim() !== ''),
        certifications: formData.certifications.filter(c => c.cert_name.trim() !== ''),
      };

      if (resume) {
        await resumeAPI.updateResume(resume.resume_id, payload);
        setMessage('Resume updated successfully!');
      } else {
        await resumeAPI.createResume(payload);
        setMessage('Resume created successfully!');
      }

      setIsEditing(false);
      fetchResume();
    } catch (error) {
      console.error('Error saving resume:', error);
      setMessage('Failed to save resume');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    fetchResume();
  };

  if (loading) {
    return <div className={styles.loading}>Loading resume...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>My Resume</h1>
        {!isEditing && resume && (
          <button onClick={() => setIsEditing(true)} className={styles.editBtn}>
            Edit Resume
          </button>
        )}
      </div>

      {message && (
        <div className={message.includes('success') ? styles.success : styles.error}>
          {message}
        </div>
      )}

      <div className={styles.resumeCard}>
        {isEditing ? (
          <div className={styles.form}>
            {/* About Me */}
            <div className={styles.section}>
              <h2>About Me</h2>
              <div className={styles.formGroup}>
                <textarea
                  name="about_me"
                  value={formData.about_me}
                  onChange={handleChange}
                  placeholder="Tell us about yourself..."
                  rows="5"
                  disabled={saving}
                />
              </div>
            </div>

            {/* Skills */}
            <div className={styles.section}>
              <h2>Skills</h2>
              {formData.skills.map((skill, index) => (
                <div key={index} className={styles.arrayItem}>
                  <input
                    type="text"
                    value={skill.skill_name}
                    onChange={(e) => updateSkill(index, e.target.value)}
                    placeholder="e.g. React, Python, AWS"
                    disabled={saving}
                  />
                  {formData.skills.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeSkill(index)}
                      className={styles.removeBtn}
                      disabled={saving}
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addSkill}
                className={styles.addBtn}
                disabled={saving}
              >
                + Add Skill
              </button>
            </div>

            {/* Education */}
            <div className={styles.section}>
              <h2>Education</h2>
              {formData.education.map((edu, index) => (
                <div key={index} className={styles.educationItem}>
                  <div className={styles.formRow}>
                    <div className={styles.formGroup}>
                      <label>School Name</label>
                      <input
                        type="text"
                        value={edu.school_name}
                        onChange={(e) => updateEducation(index, 'school_name', e.target.value)}
                        placeholder="University Name"
                        disabled={saving}
                      />
                    </div>
                    <div className={styles.formGroup}>
                      <label>Degree</label>
                      <input
                        type="text"
                        value={edu.degree}
                        onChange={(e) => updateEducation(index, 'degree', e.target.value)}
                        placeholder="Bachelor's, Master's, etc."
                        disabled={saving}
                      />
                    </div>
                  </div>
                  <div className={styles.formGroup}>
                    <label>Field of Study</label>
                    <input
                      type="text"
                      value={edu.field_of_study}
                      onChange={(e) => updateEducation(index, 'field_of_study', e.target.value)}
                      placeholder="Computer Science, Business, etc."
                      disabled={saving}
                    />
                  </div>
                  {formData.education.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeEducation(index)}
                      className={styles.removeBtn}
                      disabled={saving}
                    >
                      Remove Education
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addEducation}
                className={styles.addBtn}
                disabled={saving}
              >
                + Add Education
              </button>
            </div>

            {/* Certifications */}
            <div className={styles.section}>
              <h2>Certifications</h2>
              {formData.certifications.map((cert, index) => (
                <div key={index} className={styles.certItem}>
                  <div className={styles.formRow}>
                    <div className={styles.formGroup}>
                      <label>Certification Name</label>
                      <input
                        type="text"
                        value={cert.cert_name}
                        onChange={(e) => updateCertification(index, 'cert_name', e.target.value)}
                        placeholder="AWS Certified, etc."
                        disabled={saving}
                      />
                    </div>
                    <div className={styles.formGroup}>
                      <label>Issuing Organization</label>
                      <input
                        type="text"
                        value={cert.issuing_organization}
                        onChange={(e) => updateCertification(index, 'issuing_organization', e.target.value)}
                        placeholder="Amazon, Google, etc."
                        disabled={saving}
                      />
                    </div>
                  </div>
                  {formData.certifications.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeCertification(index)}
                      className={styles.removeBtn}
                      disabled={saving}
                    >
                      Remove Certification
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addCertification}
                className={styles.addBtn}
                disabled={saving}
              >
                + Add Certification
              </button>
            </div>

            {/* Actions */}
            <div className={styles.actions}>
              <button
                onClick={handleCancel}
                className={styles.cancelBtn}
                disabled={saving}
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className={styles.saveBtn}
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save Resume'}
              </button>
            </div>
          </div>
        ) : (
          <div className={styles.viewMode}>
            {!resume ? (
              <div className={styles.emptyState}>
                <p>You haven't created a resume yet</p>
                <button onClick={() => setIsEditing(true)} className={styles.createBtn}>
                  Create Resume
                </button>
              </div>
            ) : (
              <>
                {resume.about_me && (
                  <div className={styles.section}>
                    <h2>About Me</h2>
                    <p>{resume.about_me}</p>
                  </div>
                )}

                {resume.resume_skills?.length > 0 && (
                  <div className={styles.section}>
                    <h2>Skills</h2>
                    <div className={styles.skillsList}>
                      {resume.resume_skills.map((rs, index) => (
                        <span key={index} className={styles.skillBadge}>
                          {rs.skill.skill_name}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {resume.educations?.length > 0 && (
                  <div className={styles.section}>
                    <h2>Education</h2>
                    {resume.educations.map((edu, index) => (
                      <div key={index} className={styles.educationView}>
                        <h3>{edu.school_name}</h3>
                        <p>
                          {edu.degree} in {edu.field_of_study}
                        </p>
                      </div>
                    ))}
                  </div>
                )}

                {resume.certifications?.length > 0 && (
                  <div className={styles.section}>
                    <h2>Certifications</h2>
                    {resume.certifications.map((cert, index) => (
                      <div key={index} className={styles.certView}>
                        <h3>{cert.cert_name}</h3>
                        <p>{cert.issuing_organization}</p>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
