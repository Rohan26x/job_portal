'use client';

import { useState, useEffect } from 'react';
import { recruiterAPI } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';
import styles from './Profile.module.css';

export default function RecruiterProfilePage() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    company_name: '',
    company_description: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await recruiterAPI.getMyProfile();
      setProfile(response.data);
      setFormData({
        company_name: response.data.company_name || '',
        company_description: response.data.company_description || '',
      });
    } catch (error) {
      console.error('Error fetching profile:', error);
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

  const handleSave = async () => {
    setSaving(true);
    setMessage('');

    try {
      await recruiterAPI.updateProfile(formData);
      setMessage('Profile updated successfully!');
      setIsEditing(false);
      fetchProfile();
    } catch (error) {
      console.error('Error updating profile:', error);
      setMessage('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setFormData({
      company_name: profile.company_name || '',
      company_description: profile.company_description || '',
    });
  };

  if (loading) {
    return <div className={styles.loading}>Loading profile...</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>My Profile</h1>

      <div className={styles.profileCard}>
        <div className={styles.section}>
          <h2>Account Information</h2>
          <div className={styles.infoRow}>
            <span className={styles.label}>Email:</span>
            <span className={styles.value}>{user?.email}</span>
          </div>
          <div className={styles.infoRow}>
            <span className={styles.label}>User Type:</span>
            <span className={styles.value}>Recruiter</span>
          </div>
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader}>
            <h2>Company Information</h2>
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className={styles.editBtn}
              >
                Edit Profile
              </button>
            )}
          </div>

          {message && (
            <div className={message.includes('success') ? styles.success : styles.error}>
              {message}
            </div>
          )}

          {isEditing ? (
            <div className={styles.form}>
              <div className={styles.formGroup}>
                <label htmlFor="company_name">Company Name</label>
                <input
                  type="text"
                  id="company_name"
                  name="company_name"
                  value={formData.company_name}
                  onChange={handleChange}
                  disabled={saving}
                />
              </div>

              <div className={styles.formGroup}>
                <label htmlFor="company_description">Company Description</label>
                <textarea
                  id="company_description"
                  name="company_description"
                  value={formData.company_description}
                  onChange={handleChange}
                  rows="6"
                  disabled={saving}
                />
              </div>

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
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </div>
          ) : (
            <div>
              <div className={styles.infoRow}>
                <span className={styles.label}>Company Name:</span>
                <span className={styles.value}>
                  {profile?.company_name || 'Not provided'}
                </span>
              </div>
              <div className={styles.infoRow}>
                <span className={styles.label}>Company Description:</span>
                <span className={styles.value}>
                  {profile?.company_description || 'Not provided'}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
