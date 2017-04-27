package org.srvvp.knowledgetree.entity;
// Generated 5 Apr, 2017 12:15:43 PM by Hibernate Tools 3.2.4.GA

import javax.persistence.Column;
import javax.persistence.Embeddable;
import org.hibernate.validator.Length;
import org.hibernate.validator.NotNull;

/**
 * SubjectHasWorkId generated by hbm2java
 */
@Embeddable
public class SubjectHasWorkId implements java.io.Serializable {

	private String subject;
	private String work;
	private String workSubjectRelation;

	public SubjectHasWorkId() {
	}

	public SubjectHasWorkId(String subject, String work,
			String workSubjectRelation) {
		this.subject = subject;
		this.work = work;
		this.workSubjectRelation = workSubjectRelation;
	}

	@Column(name = "Subject", nullable = false, length = 20)
	@NotNull
	@Length(max = 20)
	public String getSubject() {
		return this.subject;
	}

	public void setSubject(String subject) {
		this.subject = subject;
	}

	@Column(name = "Work", nullable = false, length = 20)
	@NotNull
	@Length(max = 20)
	public String getWork() {
		return this.work;
	}

	public void setWork(String work) {
		this.work = work;
	}

	@Column(name = "work_subject_relation", nullable = false, length = 20)
	@NotNull
	@Length(max = 20)
	public String getWorkSubjectRelation() {
		return this.workSubjectRelation;
	}

	public void setWorkSubjectRelation(String workSubjectRelation) {
		this.workSubjectRelation = workSubjectRelation;
	}

	public boolean equals(Object other) {
		if ((this == other))
			return true;
		if ((other == null))
			return false;
		if (!(other instanceof SubjectHasWorkId))
			return false;
		SubjectHasWorkId castOther = (SubjectHasWorkId) other;

		return ((this.getSubject() == castOther.getSubject()) || (this
				.getSubject() != null
				&& castOther.getSubject() != null && this.getSubject().equals(
				castOther.getSubject())))
				&& ((this.getWork() == castOther.getWork()) || (this.getWork() != null
						&& castOther.getWork() != null && this.getWork()
						.equals(castOther.getWork())))
				&& ((this.getWorkSubjectRelation() == castOther
						.getWorkSubjectRelation()) || (this
						.getWorkSubjectRelation() != null
						&& castOther.getWorkSubjectRelation() != null && this
						.getWorkSubjectRelation().equals(
								castOther.getWorkSubjectRelation())));
	}

	public int hashCode() {
		int result = 17;

		result = 37 * result
				+ (getSubject() == null ? 0 : this.getSubject().hashCode());
		result = 37 * result
				+ (getWork() == null ? 0 : this.getWork().hashCode());
		result = 37
				* result
				+ (getWorkSubjectRelation() == null ? 0 : this
						.getWorkSubjectRelation().hashCode());
		return result;
	}

}